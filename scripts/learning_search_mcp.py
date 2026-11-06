"""Read-only, explicitly scoped text search for Claude hosts without Grep/Glob."""
import argparse
import asyncio
import json
import os
from pathlib import Path


def read_scoped(scope_config,file_path,offset=1,limit=800):
    requested=Path(file_path);target=requested.resolve()
    permitted=False
    for definition in scope_config.values():
        root=Path(definition['root']).resolve()
        if not target.is_relative_to(root):continue
        if 'files' in definition and target not in {Path(p).resolve() for p in definition['files']}:continue
        permitted=True;break
    if not permitted or requested.is_symlink():raise PermissionError('File is outside the configured evidence list')
    if not target.is_file():raise FileNotFoundError('Listed evidence file does not exist')
    if target.stat().st_size>8*1024*1024:raise ValueError('Read limit is 8 MiB')
    offset=max(1,int(offset));limit=max(1,min(int(limit),1200))
    lines=target.read_text(encoding='utf-8-sig').splitlines()
    end=min(len(lines),offset-1+limit)
    return {'file':str(target),'total_lines':len(lines),'start_line':offset,'end_line':end,
            'content':'\n'.join(f'{i+1}\t{line}' for i,line in enumerate(lines[offset-1:end],offset-1)),
            'has_more':end<len(lines)}


def search(scope_config, query, scope='', max_results=40):
    if not query or len(query)>300:raise ValueError('Provide a literal symbol/text of 1..300 characters')
    limit=max(1,min(int(max_results),100));matches=[];skipped=[];total=0
    for name,definition in scope_config.items():
        if scope and name!=scope:continue
        root=Path(definition['root']).resolve()
        files=[Path(p) for p in definition['files']] if 'files' in definition else sorted(root.rglob('*'))
        for file in files:
            resolved=file.resolve()
            if not resolved.is_relative_to(root) or file.is_symlink():
                skipped.append({'path':str(file),'reason':'outside scope or symlink'});continue
            if not file.is_file() or '.codewiki' in file.parts or '__pycache__' in file.parts:continue
            if file.suffix.lower() not in {'.c','.cpp','.cc','.cxx','.h','.hpp','.hh','.hxx','.inc','.inl','.md','.txt','.json','.src'} and file.name not in {'Makefile','CMakeLists.txt'}:continue
            if file.stat().st_size>8*1024*1024:
                skipped.append({'path':str(file),'reason':'larger than 8 MiB'});continue
            try:lines=file.read_text(encoding='utf-8-sig').splitlines()
            except (OSError,UnicodeError) as error:
                skipped.append({'path':str(file),'reason':type(error).__name__});continue
            for number,line in enumerate(lines,1):
                if query in line:
                    total+=1
                    if len(matches)<limit:matches.append({'scope':name,'file':str(resolved),
                        'relative_path':resolved.relative_to(root).as_posix(),'line':number,
                        'text':line[:500],'line_truncated':len(line)>500})
    if scope and scope not in scope_config:raise ValueError('Unknown scope')
    return {'query':query,'matching_lines':total,'matches':matches,'truncated':total>limit,'skipped':skipped}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scopes',type=Path,required=True);args=parser.parse_args()
    scopes=json.loads(args.scopes.read_text(encoding='utf-8'))
    for name in list(os.environ):
        if name.startswith(('ANTHROPIC_','OPENAI_','LITELLM_')):del os.environ[name]
    os.environ.update(PYTHON_DOTENV_DISABLED='1',OTEL_SDK_DISABLED='true')
    from mcp.server.fastmcp import FastMCP
    server=FastMCP('learning')
    @server.tool()
    def read_text(file_path:str,offset:int=1,limit:int=800)->dict:
        """Read a listed local evidence file with real one-based line numbers.

        Only configured roots/file allowlists are accessible. No directory
        listing, shell, network, writes, or arbitrary filesystem access.
        """
        return read_scoped(scopes,file_path,offset,limit)
    @server.tool()
    def search_text(query:str,scope:str='',max_results:int=40)->dict:
        """Search a literal symbol/text in the configured source/context/manual/wiki scope.

        Returns real file paths and one-based line numbers. Use Read at these
        locations for complete definitions. No shell, writes, regex, or network.
        """
        return search(scopes,query,scope,max_results)
    loop=asyncio.new_event_loop()
    def audit(event,arguments):
        if event in {'socket.connect','socket.connect_ex','socket.getaddrinfo','socket.sendto'}:
            raise PermissionError('Local search has no network access')
    sys_import=__import__('sys');sys_import.addaudithook(audit)
    try:loop.run_until_complete(server.run_stdio_async())
    finally:loop.close()


if __name__=='__main__':main()
