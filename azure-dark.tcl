# Copyright (c) 2021 rdbende <rdbende@gmail.com>
# Azure theme is a beautiful modern ttk theme inspired by Microsoft's fluent design.
package require Tk 8.6
namespace eval ttk::theme::azure-dark {

    variable version 1.3
    package provide ttk::theme::azure-dark $version
    variable colors
    array set colors {
        -fg             "#ffffff"
        -bg             "#333333"
        -disabledfg     "#ffffff"
        -disabledbg     "#737373"
        -selectfg       "#ffffff"
        -selectbg       "#737373"
    }

    proc LoadImages {imgdir} {
        variable I
        foreach file [glob -directory $imgdir *.png] {
            set img [file tail [file rootname $file]]
            set I($img) [image create photo -file $file -format png]
        }
    }

    LoadImages [file join [file dirname [info script]] azure-dark]

    # Settings
    ttk::style theme create azure-dark -parent default -settings {
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-bg) \
            -focuscolor $colors(-selectbg) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -fieldbackground $colors(-selectbg) \
            -font TkDefaultFont \
            -borderwidth 1 \
            -relief flat

        ttk::style map . -foreground [list disabled $colors(-disabledfg)]

        tk_setPalette background [ttk::style lookup . -background] \
            foreground [ttk::style lookup . -foreground] \
            highlightColor [ttk::style lookup . -focuscolor] \
            selectBackground [ttk::style lookup . -selectbackground] \
            selectForeground [ttk::style lookup . -selectforeground] \
            activeBackground [ttk::style lookup . -selectbackground] \
            activeForeground [ttk::style lookup . -selectforeground]
        option add *font [ttk::style lookup . -font]


        # Layouts

        ttk::style layout AccentButton {
            AccentButton.button -children {
                AccentButton.padding -children {
                    AccentButton.label -side left -expand true
                } 
            }
        }
        # Elements

        # Button
        ttk::style configure TButton -padding {8 4 8 4} -width -10 -anchor center

        ttk::style element create Button.button image \
            [list $I(rect-basic) \
                disabled $I(rect-basic) \
                pressed $I(rect-basic) \
                active $I(button-hover) \
            ] -border 4 -sticky ewns


        # AccentButton
        ttk::style configure AccentButton -padding {8 4 8 4} -width -10 -anchor center

        ttk::style element create AccentButton.button image \
            [list $I(rect-accent) \
                disabled $I(rect-accent-hover) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
            ] -border 4 -sticky ewns
        # Entry
        ttk::style element create Entry.field \
            image [list $I(box-basic) \
                {focus hover} $I(box-accent) \
                invalid $I(box-invalid) \
                disabled $I(box-basic) \
                focus $I(box-accent) \
                hover $I(box-hover) \
            ] -border 5 -padding {8} -sticky news
    }
}