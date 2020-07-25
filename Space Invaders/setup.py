import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Space Invaders",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["alien.png","background.png",
                                            "bullet.png","coronavirus.png",
                                            "space-invaders.png","background.wav",
                                            "laser.wav","HighScore.txt"]}},
    executables = executables

    )
