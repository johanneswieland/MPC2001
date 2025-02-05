# shell script that deletes all the input and output folders in the subdirectories of the current directory

# find all subdirectories in the current directory
for dir in $(find . -maxdepth 1 -type d); do
    # if the directory is external_data, only remove its input folder
    if [ "$dir" = "./external_data" ]; then
        rm -rf "$dir/input"
    else
        # for all other directories, delete both input and output folders
        rm -rf "$dir/input" "$dir/output"
    fi
done
