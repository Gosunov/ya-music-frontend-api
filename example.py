import ya_music
import sys

args = sys.argv
if len(args) != 2:
    print('Usage: python3 %s "<Session_id>"' % args[0])
    exit(0)

session_id = args[1]
ya_music = ya_music.Client(session_id) 

print('Before:', *ya_music.get_history()[:5], sep='\n')
ya_music.add_to_history('2269771:225060') # Window Movie Sound Effects 2sec
print()
print('After:', *ya_music.get_history()[:5], sep='\n')