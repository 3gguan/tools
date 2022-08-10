#include <pwd.h>
#include <stdio.h>
#include <errno.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>

char *names[] = {
    "root", "sqlqa", "gbasedbt", NULL
};

int ver_args(char *list[], char *string)
{
    while (*list != NULL)
    {
        if (!strncmp(*list, string, strlen(*list)))
        {
            return 1;
        }
        else
        {
            list++;
        }
    }

    return 0;
}

int main(int argc, char *argv[])
{
    struct passwd *pword;
    if (argc < 3)
    {
        printf("Usage: %s login <program_name>\r\n", *argv++);
        return -1;
    }

    if (ver_args(&names[0], argv[1]))
    {
        if ((pword = getpwnam(argv[1])) == NULL)
        {
            printf("\"%s\" is not a user on this system\r\n", argv[1]);
            return -1;
        }
        if (setgid(pword->pw_gid) < 0)
        {
            printf("Permission denied - Cannot set group ID\r\n");
            return -1;
        }
        if (setuid(pword->pw_uid) < 0)
        {
            printf("Permission denied - Cannot set userid\r\n");
            return -1;
        }

        execvp(argv[2], &argv[2]);

        printf("%s: %s command not found or bad permission\r\n", argv[0], argv[2]);
        return -1;
    }
    else
    {
        printf("Permission denied\r\n");
        return -1;
    }
}
