def writeText(txt):
    """
Write text with package logging into to locked file
"""
    lg = open ('fileName', 'a')
    # lock the file
    fcntl.flock (lg.fileno(), fcntl.LOCK_EX)
    # seek to the end of the file
    lg.seek (0, 2)
    # write the entry
    lg.write (txt + "\n")
    # close the file
    lg.close ()
    return


writeText("foo")
