dnl copied from pygtk
dnl
dnl a macro to check for ability to create python extensions
dnl  AM_CHECK_PYTHON_HEADERS([ACTION-IF-POSSIBLE], [ACTION-IF-NOT-POSSIBLE])
dnl function also defines PYTHON_INCLUDES
AC_DEFUN([AM_CHECK_PYTHON_HEADERS],
[
AC_REQUIRE([AM_PATH_PYTHON])
AC_MSG_CHECKING(for python development headers)
dnl Deduce PYTHON_INCLUDES for Python 3
py_prefix=`$PYTHON -c "import sys; print(sys.prefix)"`
py_exec_prefix=`$PYTHON -c "import sys; print(sys.exec_prefix)"`
py_version=`$PYTHON -c "import sysconfig; print(sysconfig.get_python_version())"`
py_abi_tag=`$PYTHON -c "import sysconfig; print(sysconfig.get_config_var('ABIFLAGS'))"`
PYTHON_INCLUDES="-I${py_prefix}/include/python${py_version}${py_abi_tag} -I${py_prefix}/include/python${py_version}"
if test "$py_prefix" != "$py_exec_prefix"; then
  PYTHON_INCLUDES="$PYTHON_INCLUDES -I${py_exec_prefix}/include/python${py_version}${py_abi_tag} -I${py_exec_prefix}/include/python${py_version}"
fi
AC_SUBST(PYTHON_INCLUDES)
dnl Check if the headers exist
save_CPPFLAGS="$CPPFLAGS"
CPPFLAGS="$CPPFLAGS $PYTHON_INCLUDES"
AC_CHECK_HEADERS([Python.h], [AC_MSG_RESULT(found)], [AC_MSG_RESULT(not found); $2])
CPPFLAGS="$save_CPPFLAGS"
])

dnl copied and modified from gnome-python
dnl
dnl AM_CHECK_PYMOD(MODNAME [,VERSION, VERSION_MATCHER [,ACTION-IF-FOUND [,ACTION-IF-NOT-FOUND]]])
dnl Check if a module of a particular version is visible to python.
AC_DEFUN([AM_CHECK_PYMOD],
[
AC_REQUIRE([AM_PATH_PYTHON])
py_mod_var=`echo $1 | sed 's/[^a-zA-Z0-9_]/_/g'`
AC_MSG_CHECKING(for python module $1 ifelse([$2],[],,[>= $2]))
AC_CACHE_VAL([py_cv_mod_$py_mod_var], [
ifelse([$2],[], [
  prog="import sys
try:
    import $1
except ImportError:
    sys.exit(1)
sys.exit(0)"
], [
  prog="import sys
try:
    import $1
    mod_version = getattr($1, '__version__', 'unknown')
    from distutils.version import LooseVersion as LV
    if LV(mod_version) < LV('$2'):
        sys.exit(1)
except ImportError:
    sys.exit(1)
sys.exit(0)"
])
if $PYTHON -c "$prog" > /dev/null 2>&1; then
  eval "py_cv_mod_$py_mod_var=yes"
else
  eval "py_cv_mod_$py_mod_var=no"
fi
])
py_val=`eval "echo \\$$py_cv_mod_$py_mod_var"`
if test "x$py_val" != xno; then
  AC_MSG_RESULT(yes)
  ifelse([$4], [],, [$4])
else
  AC_MSG_RESULT(no)
  ifelse([$5], [],, [$5])
fi
])
dnl check for python
AC_DEFUN([LIBGPOD_CHECK_PYTHON],
[
    dnl aclocal-1.7 is missing this when version is used in AM_PATH_PYTHON, fudge it
    am_display_PYTHON=python

    AC_ARG_WITH(python,
        AC_HELP_STRING([--with-python=PATH],
            [build python bindings [[default=yes]]]),
        [with_python=$withval],[with_python=yes])

    AC_MSG_CHECKING(whether to build python bindings)
    if test "X$with_python" != Xno; then
        if test "X$with_python" != Xyes; then
            PYTHON=$with_python
        fi
        with_python=yes
    fi
    AC_MSG_RESULT($with_python)

    if test "X$with_python" = Xyes; then
        if test -z "$PYTHON"; then
            AC_PATH_PROG(PYTHON, python)
        fi
    
        if test -n "$PYTHON"; then
            AM_PATH_PYTHON($PYTHON_MIN_VERSION)
            AM_CHECK_PYTHON_HEADERS(with_python="yes",with_python="no")
    
            if test "X$with_python" = Xyes; then
                dnl test for python ldflags
                dnl copied from the Redland RDF bindings, http://librdf.org/
                if test `uname` = Darwin; then
                    PYTHON_LDFLAGS="-Wl,-F. -Wl,-F. -bundle"
                    if $PYTHON -c 'import sys, string; sys.exit(string.find(sys.prefix,"Framework")+1)'; then
                        :
                    else
                        PYTHON_LDFLAGS="$PYTHON_LDFLAGS -framework Python"
                    fi
                else
                    PYTHON_LDFLAGS="-shared"
                fi
                AC_SUBST(PYTHON_LDFLAGS)

                dnl check for mutagen module >= $PYTHON_MUTAGEN_MIN_VERSION
                AM_CHECK_PYMOD(mutagen,$PYTHON_MUTAGEN_MIN_VERSION,mutagen.version_string,,with_python=no)

                dnl this test should perhaps be re-enabled, but only produce a warning -- tmz
                dnl if test "X$have_gdkpixbuf" = "Xyes" -a "X$have_pygobject" = "Xyes"; then
                dnl     dnl check for gtk module >= $PYTHON_GTK_MIN_VERSION
                dnl     AM_CHECK_PYMOD(gtk,$PYTHON_GTK_MIN_VERSION,'.'.join(map(str, gtk.ver)),,with_python=no)
                dnl fi

                dnl check for swig
                if test "X$with_python" = Xyes; then
                    AX_PKG_SWIG($SWIG_MIN_VERSION, has_swig=yes, has_swig=no)
                    with_python="$has_swig"
                fi
            fi
        else
            AC_MSG_WARN(python not found.  try --with-python=/path/to/python)
            with_python="no"
        fi
    fi
    AM_CONDITIONAL(HAVE_PYTHON, test x$with_python = xyes)
])dnl

