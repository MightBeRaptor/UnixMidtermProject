#!/bin/bash

GROUP_NAME="developer"
USER1="alice"
USER2="bob"
USER3="charlie"

if ! getent group "$GROUP_NAME" > /dev/null; then
    groupadd "$GROUP_NAME"
    echo "Group '$GROUP_NAME' created."
else
    echo "Group '$GROUP_NAME' already exists."
fi

create_user() {
    local USERNAME=$1
    if ! id "$USERNAME" &>/dev/null; then
        useradd -m -G "$GROUP_NAME" "$USERNAME"
        echo "User '$USERNAME' created and added to '$GROUP_NAME'."
    else
        echo "User '$USERNAME' already exists."
    fi
}

create_user "$USER1"
create_user "$USER2"
create_user "$USER3"