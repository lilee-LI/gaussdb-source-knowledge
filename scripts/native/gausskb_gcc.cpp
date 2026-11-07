// SPDX-License-Identifier: MIT
// Read the matching GCC frontend's trees without code generation or rewriting source.
#include "gcc-plugin.h"
#include "plugin-version.h"
#include "tree.h"
#include "tree-iterator.h"
#include "function.h"
#include "input.h"
#include "langhooks.h"
#include "tree-pretty-print.h"
#ifdef GAUSSKB_CXX
#include "cp/cp-tree.h"
#endif
#include <cstdio>
#include <cstring>
#include <string>
#include <unordered_map>
#include <vector>

int plugin_is_GPL_compatible;
static FILE* output;
static std::vector<std::string> roots;
static std::unordered_map<unsigned, bool> emitted;
struct source_origin { std::string file; long physical; unsigned logical; };
static std::vector<source_origin> origins;
static std::vector<unsigned> includers;

static std::string quote(const char* value) {
    std::string result = "\"";
    if (value) for (const unsigned char* p = (const unsigned char*)value; *p; ++p) {
        if (*p == '"' || *p == '\\') { result += '\\'; result += *p; }
        else if (*p < 32) { char text[8]; snprintf(text, sizeof(text), "\\u%04x", *p); result += text; }
        else result += *p;
    }
    return result + '"';
}

static bool in_repository(const char* file) {
    if (!file || file[0] == '<') return false;
    for (const auto& root : roots)
        if (!strncmp(file, root.c_str(), root.size()) && file[root.size()] == '/') return true;
    return false;
}

// Line-map transitions retain the active physical input even when #line
// changes its displayed name, repeats line numbers, or skips inactive branches.
static const source_origin& physical_origin(const line_map_ordinary* map) {
    for (unsigned i = origins.size(); i < LINEMAPS_ORDINARY_USED(line_table); ++i) {
        const auto* current = LINEMAPS_ORDINARY_MAP_AT(line_table, i);
        source_origin value = {LINEMAP_FILE(current), (long)LINEMAP_LINE(current), LINEMAP_LINE(current)};
        if (current->reason == LC_ENTER) {
            if (i) includers.push_back(i - 1);
        } else if (current->reason == LC_LEAVE && !includers.empty()) {
            value = origins[includers.back()];
            includers.pop_back();
            value.physical += (long)LINEMAP_LINE(current) - value.logical;
            value.logical = LINEMAP_LINE(current);
        } else if (i) {
            const auto* previous = LINEMAPS_ORDINARY_MAP_AT(line_table, i - 1);
            value = origins.back();
            value.physical += (long)SOURCE_LINE(previous, current->start_location - 1) - value.logical;
            value.logical = LINEMAP_LINE(current);
        }
        origins.push_back(value);
    }
    unsigned index = map - LINEMAPS_ORDINARY_MAPS(line_table);
    return origins[index];
}

static bool repository_location(location_t loc) {
    const line_map_ordinary* map = nullptr;
    linemap_resolve_location(line_table, get_pure_location(loc), LRK_MACRO_EXPANSION_POINT, &map);
    return map && in_repository(physical_origin(map).file.c_str());
}

static std::string position(location_t loc, bool spelling = false) {
    const line_map_ordinary* map = nullptr;
    linemap_resolve_location(line_table, get_pure_location(loc),
        spelling ? LRK_SPELLING_LOCATION : LRK_MACRO_EXPANSION_POINT, &map);
    expanded_location p = spelling ? expand_location_to_spelling_point(loc) : expand_location(expansion_point_location(loc));
    source_origin origin = map ? physical_origin(map) : source_origin{"",0,0};
    return "{\"file\":" + quote(p.file) + ",\"line\":" + std::to_string(p.line)
        + ",\"column\":" + std::to_string(p.column)
        + ",\"physical_file\":" + quote(origin.file.c_str())
        + ",\"physical_line\":" + std::to_string(origin.physical + (long)p.line - origin.logical) + "}";
}

static unsigned symbol(tree decl, bool definition = false, int end = 0, location_t end_loc = UNKNOWN_LOCATION) {
    if (!decl || TREE_CODE(decl) != FUNCTION_DECL) return 0;
    expanded_location loc = expand_location(DECL_SOURCE_LOCATION(decl));
    if (!repository_location(DECL_SOURCE_LOCATION(decl))) return 0;
    unsigned uid = DECL_UID(decl);
    auto old = emitted.find(uid);
    if (old != emitted.end() && (old->second || !definition)) return uid;
    emitted[uid] = definition;
    const char* name = DECL_NAME(decl) ? IDENTIFIER_POINTER(DECL_NAME(decl)) : "";
    const char* kind = "function_decl";
    if (DECL_CXX_CONSTRUCTOR_P(decl)) kind = "constructor";
    else if (DECL_CXX_DESTRUCTOR_P(decl)) kind = "destructor";
    else if (DECL_CONTEXT(decl) && TYPE_P(DECL_CONTEXT(decl))) kind = "cxx_method";
    std::string human_name(name);
    if (DECL_CXX_CONSTRUCTOR_P(decl) || DECL_CXX_DESTRUCTOR_P(decl)) {
        tree type_name = DECL_CONTEXT(decl) ? TYPE_NAME(DECL_CONTEXT(decl)) : NULL_TREE;
        if (type_name && TREE_CODE(type_name) == TYPE_DECL) type_name = DECL_NAME(type_name);
        if (type_name && TREE_CODE(type_name) == IDENTIFIER_NODE)
            human_name = std::string(DECL_CXX_DESTRUCTOR_P(decl) ? "~" : "") + IDENTIFIER_POINTER(type_name);
    }
    const char* printable = lang_hooks.decl_printable_name(decl, 2);
    std::string spelling = quote(printable);
    // Mangled names retain overloads, C linkage and template instantiation identity.
    std::string abi = quote(IDENTIFIER_POINTER(DECL_ASSEMBLER_NAME(decl)));
#ifdef GAUSSKB_CXX
    std::string type = quote(type_as_string(TREE_TYPE(decl), TFF_PLAIN_IDENTIFIER));
#else
    char* type_text = print_generic_expr_to_str(TREE_TYPE(decl));
    std::string display(type_text);
    free(type_text);
    // GCC's generic printer embeds TU-local type UIDs, which are not semantic types.
    size_t at = 0;
    while ((at = display.find("<T", at)) != std::string::npos) {
        size_t end = display.find('>', at + 2);
        if (end == std::string::npos) break;
        display.erase(at, end - at + 1);
    }
    std::string type = quote(display.c_str());
#endif
    fprintf(output, "{\"event\":\"symbol\",\"uid\":%u,\"name\":%s,\"spelling\":%s,"
        "\"abi\":%s,\"type\":%s,\"kind\":%s,\"position\":%s,\"end\":%d,\"external\":%s,"
        "\"definition\":%s,\"implicit\":%s,\"end_position\":%s}\n", uid, quote(human_name.c_str()).c_str(), spelling.c_str(),
        abi.c_str(), type.c_str(), quote(kind).c_str(), position(DECL_SOURCE_LOCATION(decl)).c_str(),
        end > loc.line ? end : loc.line, TREE_PUBLIC(decl) ? "true" : "false",
        definition ? "true" : "false", DECL_ARTIFICIAL(decl) ? "true" : "false",
        position(end_loc == UNKNOWN_LOCATION ? DECL_SOURCE_LOCATION(decl) : end_loc).c_str());
    return uid;
}

struct context { tree owner; int end; const char* file; location_t end_loc; };
static tree visit(tree* pointer, int* descend, void* data) {
    tree value = *pointer;
    if (!value) return NULL_TREE;
    context* ctx = (context*)data;
    if (DECL_P(value) || TYPE_P(value)) { *descend = 0; return NULL_TREE; }
    location_t loc = EXPR_P(value) ? EXPR_LOCATION(value) : UNKNOWN_LOCATION;
    expanded_location where = expand_location(loc);
    if (where.file && ctx->file && !strcmp(where.file, ctx->file) && where.line > ctx->end) {
        ctx->end = where.line;
        ctx->end_loc = loc;
    }
    tree target = NULL_TREE;
    bool call = TREE_CODE(value) == CALL_EXPR;
    bool indirect = false, virtual_call = false;
    if (call) {
        target = get_callee_fndecl(value);
        tree fn = CALL_EXPR_FN(value);
        virtual_call = fn && TREE_CODE(fn) == OBJ_TYPE_REF;
        indirect = target == NULL_TREE;
    }
#ifdef GAUSSKB_CXX
    if (TREE_CODE(value) == AGGR_INIT_EXPR) {
        call = true;
        tree fn = AGGR_INIT_EXPR_FN(value);
        if (TREE_CODE(fn) == ADDR_EXPR) fn = TREE_OPERAND(fn, 0);
        if (TREE_CODE(fn) == FUNCTION_DECL) target = fn;
        indirect = target == NULL_TREE;
    }
#endif
    if (!call || loc == UNKNOWN_LOCATION || !repository_location(loc)) return NULL_TREE;
    unsigned callee = symbol(target);
    fprintf(output, "{\"event\":\"call\",\"owner\":%u,\"target\":%u,\"name\":%s,"
        "\"spelling_location\":%s,\"expansion_location\":%s,\"dispatch\":%s,\"implicit\":%s}\n",
        DECL_UID(ctx->owner), callee,
        quote(target && DECL_NAME(target) ? IDENTIFIER_POINTER(DECL_NAME(target)) : "").c_str(),
        position(loc, true).c_str(), position(loc).c_str(),
        quote(virtual_call ? "virtual" : indirect ? "indirect" : "direct").c_str(),
        target && DECL_ARTIFICIAL(target) ? "true" : "false");
    return NULL_TREE;
}

static void before_genericize(void* data, void*) {
    tree function = (tree)data;
    expanded_location loc = expand_location(DECL_SOURCE_LOCATION(function));
    if (!repository_location(DECL_SOURCE_LOCATION(function))) return;
    context ctx = {function, loc.line, loc.file, DECL_SOURCE_LOCATION(function)};
    tree body = DECL_SAVED_TREE(function);
#ifdef GAUSSKB_CXX
    cp_walk_tree_without_duplicates(&body, visit, &ctx);
#else
    walk_tree_without_duplicates(&body, visit, &ctx);
#endif
    if (DECL_STRUCT_FUNCTION(function)) {
        expanded_location end = expand_location(DECL_STRUCT_FUNCTION(function)->function_end_locus);
        if (DECL_STRUCT_FUNCTION(function)->function_end_locus != UNKNOWN_LOCATION)
            ctx.end_loc = DECL_STRUCT_FUNCTION(function)->function_end_locus;
        if (end.file && !strcmp(end.file, loc.file) && end.line > ctx.end) {
            ctx.end = end.line;
        }
    }
    symbol(function, true, ctx.end, ctx.end_loc);
}

static void include_file(void* data, void*) {
    fprintf(output, "{\"event\":\"include\",\"file\":%s}\n", quote((const char*)data).c_str());
}
static void finished(void*, void*) { if (output) { fclose(output); output = nullptr; } }

int plugin_init(plugin_name_args* args, plugin_gcc_version* version) {
    if (!plugin_default_version_check(version, &gcc_version)) return 1;
    const char* path = nullptr;
    for (int i = 0; i < args->argc; ++i) {
        if (!strcmp(args->argv[i].key, "output")) path = args->argv[i].value;
        else if (!strcmp(args->argv[i].key, "root")) roots.emplace_back(args->argv[i].value);
    }
    if (!path || roots.empty() || !(output = fopen(path, "w"))) return 1;
    register_callback(args->base_name, PLUGIN_PRE_GENERICIZE, before_genericize, nullptr);
    register_callback(args->base_name, PLUGIN_INCLUDE_FILE, include_file, nullptr);
    register_callback(args->base_name, PLUGIN_FINISH, finished, nullptr);
    return 0;
}
