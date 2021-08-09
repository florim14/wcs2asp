# The Encoding script

The `encoding.py` script is used to encode programs into ASP.
This script can be executed with different options some of which are
required. In general, the script has four parameters:
* `-f` - followed by the file we want to encode. This file is a .wcs file, 
meaning that this file is the weak completion of the logic program that we want
to encode. We elaborate later how this files looks [**required**].
* `-o` - followed by the observation we want to explain. This parameter is
used for the abduction case, where we need to define the observation that we
want to explain [**optional**, but **required** for the abduction case].
* `-s`  - followed by the semantics we want to do the encoding. We have her
e two options, either LS for Łukasiewicz and Gottwald semantics or K for Kleene
semantics. The default value is LS [**optional**].
* `-p`  - followed with Y for Yes or N for N. This parameter is used to
differentiate whether we want to compute the supported or all minimal models
for the L and S semantics. This parameter has no effect in the abduction case,
or when we use the encoding for the K semantics [**optional**].
* `-r` - followed by the literal that we want to reason. This parameter is
used for the abduction case, and it is the parameter that we want to reason
to [**optional**, but **required** for the abduction case].

>To add a negative literal, we write the classical negation with a `-` sign.
> For example if we want to add the negative atom of the atom `l`,
> we do with the following option `-r="-l"`.

After we run the script, it will generate a ```.lp``` file, which then
will be executed with respect to the type of problem that we want to solve.
The problem that we want to solve is encoded with respect to the mode, from
which an additional file is added when we run the solver. We have three modes:
* `mode: 1` it refers to the encoding file `clingoEncodingMinimalModels.lp` (if
we want to compute all the minimal) models under L, S, or K semantics. This
mode is executed when we do not use the `-o` parameter and the `-p` parameter
is `N`.
* `mode: 2` it refers to the encoding file `clingoEncodingSupportedModels.lp`
(if we want to compute the supported models under L or S semantics). This
mode is executed when we want to compute the knowledge minimal models that
can be computed with respect to the least fixed point operator Φ.
* `mode: 3` it refers to the encoding file
`clingoForAbductionEncodingMinimalModels.lp` (if we want to compute the
minimal explanation for the abduction case). This mode is executed for the
abduction case.

> Remark: the parameters should be used with the corresponding `clingo....lp`
> file. For example if we use the `clingoForAbductionEncodingMinimalModels.lp`
> file, we need to use the `-o` and `-r` parameters as well. These tells which
> observation we want to explain, and for which literal we want to reason.
