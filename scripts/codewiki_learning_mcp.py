"""Run a local CodeWiki stdio server without inherited model credentials/network."""
import argparse
import asyncio
import os
from pathlib import Path
import sys

parser=argparse.ArgumentParser()
parser.add_argument('--vendor',type=Path,required=True)
parser.add_argument('--cache',type=Path,required=True)
parser.add_argument('--parser-site',type=Path)
args=parser.parse_args()
for name in list(os.environ):
    if name.startswith(('ANTHROPIC_','OPENAI_','LITELLM_')):
        del os.environ[name]
os.environ.update(MERMAID_VALIDATE='0',PYTHON_DOTENV_DISABLED='1',OTEL_SDK_DISABLED='true',
    LOGFIRE_SEND_TO_LOGFIRE='false',TIKTOKEN_CACHE_DIR=str(args.cache))
sys.path.insert(0,str(args.vendor.resolve()))
if args.parser_site:sys.path.insert(0,str(args.parser_site.resolve()))
from codewiki.mcp.server import main
loop=asyncio.new_event_loop()
def audit(event,arguments):
    if event in {'socket.connect','socket.connect_ex','socket.getaddrinfo','socket.sendto'}:
        raise PermissionError('CodeWiki analysis subprocess has no network access')
sys.addaudithook(audit)
try:loop.run_until_complete(main())
finally:loop.close()
