#!/bin/bash

# Configurations
## Link to your github repo
github_repo="https://github.com/jockerz/Koleksi"

print_help() {
    echo -e "Usage \t$0 <option>"
    echo -e "Options \n\tnew : create new md and python file (Will be prompted)"
    echo -e "\thelp: print this"
    exit
}

create_files() {
    echo "Name(one line). Type the name(for .py and .md filename), followed by [ENTER]"
    printf "Name: "
    read name
    # Create markdown files
    if [ -f "${name}.md" ]; then
        echo "${name}.md is exist. Use another name"
        exit 1
    fi
    # Create python files
    if [ -f ${name}.py ]; then
        echo "${name}.py is exist. Use another name"
        exit 2
    fi
    echo "Creating ${name}.md and ${name}.py"
    echo "Type the description(one line), followed by [ENTER]"
    echo "NOTE: Please use alphanumneric (a-z and 0-9) characters only"
    printf "Desc: "
    read Desc

    echo "## $Desc" >> ${name}.md
    echo -e "\n\n[EDIT ME]\n\n" >> ${name}.md
    echo -e "\n## [<< Back to main page]($github_repo) \n" >> ${name}.md
    echo "[+] ${name}.md is created"

    echo -e "#!/usr/bin/python3 \n\nprint \"[EDIT ME]\"" >> ${name}.py
    echo "[+] ${name}.py is created"

    # replace "_EndOfExercise_" with current exercise .md url
    to_list="[${name} ~ ${Desc}](/${name}.md)"
    #to_list=`echo $to_list | sed "s/\&/\\\&/" `
    # echo $to_list # debuggin
    sed "s|_EndOfExercise_|${to_list}\n- _EndOfExercise_|" -i README.md
    # Let me know
    echo "[+] Adding the new exercise page url to README.md"
}

if [ $# -ne 1 ]; then
    print_help
fi

case $1 in
    "new")
    create_files
    ;;
    *)
    print_help
    ;;
esac
