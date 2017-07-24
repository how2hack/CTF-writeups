#include <stdio.h>
#include <stdlib.h>

int main()
{
    FILE *stream;
    char *flag;
    size_t fsize;
    int seed;
    int i;

    char *guess = "ais3{??????????????????}";

    stream = fopen("flag", "rb");

    fseek(stream, 0, SEEK_END);
    fsize = ftell(stream);
    rewind(stream);

    flag = (char *)malloc(sizeof(char) * fsize);
    fread(flag, 1, fsize, stream);
    fclose(stream);

    int seed_found = 0;

    for(seed = 1498406400; seed <= 1498492800; seed++)
    {
        srand(seed);
        for(i = 0; i < 5; i++)
        {
            int t1 = guess[i];
            int t2 = rand();
            char tmp = t1 ^ t2;
            if(tmp != flag[i])
                break;
            if(i == 4)
            {
                printf("seed: %d\n", seed);
                seed_found = 1;
            }
        }
        if(seed_found == 1)
            break;
    }

    srand(seed);
    for(i = 0; i < fsize; i++)
    {
        int t1 = flag[i];
        int t2 = rand();
        char tmp = t1 ^ t2;
        printf("%c", tmp);
    }
    printf("\n");

    free(flag);
    return 0;
}
