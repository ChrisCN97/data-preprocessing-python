# import eel

def test():
    import subprocess as sps
    proc = sps.Popen('cmd.exe', stdin=sps.PIPE, stdout=sps.PIPE, stderr=sps.PIPE)
    print(proc.stdin)
    proc.kill()

test()