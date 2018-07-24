# Permutate Settings for the ONE

The ONE's batch mode expects multiple values for different scenario runs in one
batch, but doesn't offer any method to create permutations from possible
setting values.

##### Example
Example settings:
```
setting1 = [1;2]
setting2 = [a;b]
```

###### Example of the ONE's behavior
Result: `1a` and `2b`.

###### Example of the permutation behavior
Result: `1a`, `1b`, `2a` and `2b`