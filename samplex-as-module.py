import samplex
import samplexmore
choose = input("Enter 1 for only one sample or 2 for more than 1 samples(space seperated): ")
if choose == "1":
    samplex.download_samplefocus_mp3(input("Enter SampleFocus URL: ").strip())
elif choose == "2":
    samplexmore.download_multiple(input("Enter SampleFocus URLs (space separated): ").strip().split(' '))
else:
    print("Invalid choice.")
    