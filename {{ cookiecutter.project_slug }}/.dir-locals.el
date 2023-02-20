;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((eval . (progn
                   (setq-local project-root (expand-file-name (locate-dominating-file "." ".dir-locals.el")))
                   (setq-local compile-command
                               (concat (expand-file-name "env/{{ cookiecutter.scripts_or_bin }}/doit" project-root) " -f " (expand-file-name "dodo.py" project-root)))))))
 (python-mode . ((mode . black-on-save)
                 (eval . (progn
                           (setenv "PYTHONSTARTUP" (expand-file-name "pythonrc" project-root))
                           (setenv "PYTHONPATH" project-root)
                           (setq-local gud-pdb-command-name
                                       (concat (expand-file-name "env/{{ cookiecutter.scripts_or_bin }}/python" project-root) " -m pdb main.py"))
                           (setq-local black-command
                                       (expand-file-name "env/{{ cookiecutter.scripts_or_bin }}/black" project-root))
                           (setq-local python-shell-virtualenv-root
                                       (expand-file-name "env" project-root)))))))
