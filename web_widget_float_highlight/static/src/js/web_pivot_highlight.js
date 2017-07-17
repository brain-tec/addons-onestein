odoo.define("web.pivot.float.highlight", function (require) {
    "use strict";
    var pivot_view = require("web.PivotView");
    var formats = require('web.formats');

    pivot_view.include({

        _load_my_default: function (option, parameter, load_defaults, load_value, def_value) {
            return (option && parameter) || load_defaults && load_value || def_value;
        },

        _retrieve_colors: function (opt_arg, val_arg) {
            var bg_color = null;
            var font_color = null;

            if (val_arg < opt_arg.lower_threshold) {
                bg_color = opt_arg.lower_bg_color;
                font_color = opt_arg.lower_font_color;
            } else if (opt_arg.upper_threshold < val_arg) {
                bg_color = opt_arg.upper_bg_color;
                font_color = opt_arg.upper_font_color;
            } else {
                bg_color = opt_arg.middle_bg_color;
                font_color = opt_arg.middle_font_color;
            }
            return [bg_color, font_color];
        },

        init: function () {
            this._super.apply(this, arguments);
            var my_options = false;
            try{
                my_options = JSON.parse(this.fields_view.arch.attrs.options.split("'").join('"')) || false;
            }
            catch(err){
                my_options = false;
            }

            var load_defaults = this._load_my_default(my_options, my_options.load_defaults, false, false, false);

            var options = {
                lower_threshold: this._load_my_default(my_options, my_options.lower_threshold, false, false, 0),
                upper_threshold: this._load_my_default(my_options, my_options.upper_threshold, false, false, 0),
                lower_bg_color: this._load_my_default(my_options, my_options.lower_bg_color, load_defaults, "red", "white"),
                middle_bg_color: this._load_my_default(my_options, my_options.middle_bg_color, false, false, "white"),
                upper_bg_color: this._load_my_default(my_options, my_options.upper_bg_color, load_defaults, "green", "white"),
                lower_font_color: this._load_my_default(my_options, my_options.lower_font_color, load_defaults, "white", "#666666"),
                middle_font_color: this._load_my_default(my_options, my_options.middle_font_color, false, false, "#666666"),
                upper_font_color: this._load_my_default(my_options, my_options.upper_font_color, load_defaults, "white", "#666666"),
                load_defaults: load_defaults
            };

            this.parsed_options = options;
            this.to_highlight = [];
            this.highlight_lookup = {};
        },

        willStart: function () {
            var res = this._super.apply(this, arguments);
            var self = this;

            this.fields_view.arch.children.forEach(function (field) {
                switch (field.attrs.type) {
                case 'measure':
                    if (field.attrs.highlight && field.attrs.highlight.toLowerCase() === 'true'){
                        self.to_highlight.push(true);
                        self.highlight_lookup[field.attrs.name] = true;
                    } else {
                        self.to_highlight.push(false);
                    }
                    break;
                default:
                    break;
                }
            });
            return res;
        },

        draw_rows: function ($tbody, rows) {
            var self = this,
                i, j, value, $row, $cell, $header,
                nbr_measures = this.active_measures.length,
                length = rows[0].values.length,
                display_total = this.main_col.width > 1;

            var groupby_labels = _.map(this.main_row.groupbys, function (gb) {
                return self.fields[gb.split(':')[0]].string;
            });
            var measure_types = this.active_measures.map(function (name) {
                return self.measures[name].type;
            });
            var widgets = this.widgets;

            var my_options = this.parsed_options;

            for (i = 0; i < rows.length; i++) {
                $row = $('<tr>');
                $header = $('<td>')
                    .text(rows[i].title)
                    .data('id', rows[i].id)
                    .css('padding-left', (5 + rows[i].indent * 30) + 'px')
                    .addClass(rows[i].expanded ? 'o_pivot_header_cell_opened' : 'o_pivot_header_cell_closed');
                if (rows[i].indent > 0) $header.attr('title', groupby_labels[rows[i].indent - 1]);
                $header.appendTo($row);
                for (j = 0; j < length; j++) {
                    value = formats.format_value(rows[i].values[j], {type: measure_types[j % nbr_measures], widget: widgets[j % nbr_measures]});
                    $cell = $('<td>')
                                .data('id', rows[i].id)
                                .data('col_id', rows[i].col_ids[Math.floor(j / nbr_measures)])
                                .toggleClass('o_empty', !value)
                                .text(value)
                                .addClass('o_pivot_cell_value text-right');
                    if (((j >= length - this.active_measures.length) && display_total) || i === 0){
                        $cell.css('font-weight', 'bold');
                    }
                    var val = parseFloat(value);
                    if (my_options && val && self.to_highlight[j % nbr_measures] && my_options.lower_threshold <= my_options.upper_threshold) {

                        var my_colors = this._retrieve_colors(my_options, val);
                        $cell.css({
                            "background-color": my_colors[0],
                            "color": my_colors[1]
                        });

                    }
                    $row.append($cell);
                    $cell.toggleClass('hidden-xs', j < length - this.active_measures.length);
                }
                $tbody.append($row);
            }
        },

        toggle_measure: function (field) {
            if (_.contains(this.active_measures, field)) {
                var idx = _.indexOf(this.active_measures, field);
                if (idx !== -1) this.to_highlight.splice(idx, 1);
            } else {
                if (field in this.highlight_lookup) this.to_highlight.push(true);
                else this.to_highlight.push(false);
            }

            this._super.apply(this, arguments);
        }
    });
});
