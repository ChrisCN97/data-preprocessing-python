import eel

def test():
    import subprocess
    proc = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(proc.stdin)
    proc.kill()

test()