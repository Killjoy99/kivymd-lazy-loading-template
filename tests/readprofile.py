import pstats

# Load the profile data
profile_file = "tests/loading_screen.profile"
stats = pstats.Stats(profile_file)

# Sort by cumulative time and print the stats
stats.sort_stats("tottime").print_stats(10)
