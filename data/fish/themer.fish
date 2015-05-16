function __fish_themer_needs_theme
  set cmd (commandline -opc)
  if [ (count $cmd) -gt 1 ]
    for param in (echo $cmd | sed "s/ /\n/g" | egrep "^[^-]")
      if contains $param activate delete render
        return 0
      end
    end
  end
  return 1
end

function __fish_themer_is_render
  set cmd (commandline -opc)
  if [ (count $cmd) -gt 1 ]
    for param in (echo $cmd | sed "s/ /\n/g" | egrep "^[^-]")
      if [ $param = "render" ]
        return 0
      end
    end
  end
  return 1
end

function __fish_themer_needs_command
  set cmd (commandline -opc)
  if [ (count $cmd) -eq 1 ]
    return 0
  end
  return 1
end

function __fish_themer_themes
  for theme in ~/.config/themer/*
    if [ -d $theme -a ! -L $theme ]
      set theme (basename $theme)
      if not contains $theme templates plugins
        echo (basename $theme)
      end
    end
  end
end

complete -f -c themer -n "__fish_themer_needs_command" -a "list activate render generate current delete plugins"
complete -f -c themer -n "__fish_themer_needs_theme" -a "(__fish_themer_themes)"
complete -f -c themer -n "__fish_themer_is_render" -a "all"

complete -r -c themer -s c -l config
complete -r -c themer -s t -l template
