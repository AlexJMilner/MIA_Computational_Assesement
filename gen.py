import os


if __name__ == '__main__':
    files = [f for f in os.listdir('.') if os.path.isfile(f)]

    files_c = 0

    for f in files:
        template = f"<None Include=\"..\\\\win\\\\x64\\\\{f}\" Link=\"runtimes\\\\win-x64\\\\native\\\\{f}\">\n<CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>\n</None>"

        if f.endswith(".dll"):
            files_c += 1
            print(template)

    print(files_c)