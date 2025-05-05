import asyncio
import glob
import os

plugins = glob.glob('plugins/*.smx')

async def run_subprocess(command):
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=3)
        return stdout.decode('utf-8', errors='ignore')
    except asyncio.TimeoutError:
        return ""

async def main():
    for p in plugins:
        print(p)
        pl_name = p.replace('plugins\\', '').split('.')[0]
        sp_file = pl_name + '.sp'

        command = f'java -jar lysis.jar {p}'
        result = await run_subprocess(command)

        with open(sp_file, mode='w', encoding='utf-8') as f:
            f.write(result)

        os.replace(sp_file, 'smx_decompiled/' + sp_file)

if __name__ == '__main__':
    asyncio.run(main())