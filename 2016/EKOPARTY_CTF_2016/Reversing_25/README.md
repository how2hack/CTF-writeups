#EKOPARTY CTF 2016: Reversing 25

###JVM
```
Bytecodes everywhere, reverse them.

Attachment
rev25_3100aa76fca4432f.zip
```

##Solution
A java class file, so I just have to decompile it.
Found a java decompiler website
>http://www.javadecompilers.com/

After decompile the java class file, I got this code
```
public class EKO {
    public static void main(String[] arrstring) {
        int n = 0;
        for (int i = 0; i < 1337; ++i) {
            n += i;
        }
        String string = "EKO{" + n + "}";
    }
}
```

Obviously the flag is EKO{1 + 2 + ... + 1336}

Flag:
>EKO{893116}
