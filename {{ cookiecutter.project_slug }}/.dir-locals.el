;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((eval . (progn
                   (setq-local project-root (expand-file-name (locate-dominating-file "." ".dir-locals.el")))
                   (setq-local compile-command
                               (concat (expand-file-name "env/bin/doit" project-root) " -f " (expand-file-name "dodo.py" project-root)))))))
 (python-mode . ((mode . black-on-save)
                 (eval . (progn
                           (setenv "PYTHONSTARTUP" (expand-file-name "pythonrc" project-root))
                           (setenv "PYTHONPATH" project-root)
                           ; (setq-local gud-pdb-command-name "env/bin/python -m pdb main.py")
                           (setq-local black-command
                                       (expand-file-name "env/bin/black" project-root))
                           (setq-local python-shell-virtualenv-root
                                       (expand-file-name "env" project-root)))))))
