from __future__ import division

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
from tool.Tools import Tools
import io


class DrawTools:

    @staticmethod
    def setFonts(font_size):
        matplotlib.rcParams.update({'font.size': font_size})
        matplotlib.rcParams['font.family'] = 'Times New Roman'

    @staticmethod
    def parseList2d(list2d):
        list2d = np.asarray(list2d)
        nrow = len(list2d)
        ncol = len(list2d[0])
        return list2d, nrow, ncol

    @staticmethod
    def getPlotPropertiesByListColIndex(col_index
                                    , line_style_list
                                    , line_color_list
                                    , line_marker_list
                                    , line_alpha_list):
        if line_style_list != None:
            linestyle = line_style_list[col_index - 1]
        else:
            linestyle = None

        if line_color_list != None:
            color = line_color_list[col_index - 1]
        else:
            color = None
        if line_marker_list != None:
            marker = line_marker_list[col_index - 1]
        else:
            marker = None

        if line_alpha_list != None:
            alpha = line_alpha_list[col_index - 1]
        else:
            alpha = None

        return linestyle, color, marker, alpha

    @staticmethod
    def saveFig(path):
        assert path != None
        if not path.endswith(".png"):
            path += ".png"
        Tools.createFileDirIfNotExist(path)
        plt.savefig(path)
        im = Image.open(path)
        im = DrawTools.trim(im)
        im.save('%s' % (path))
        plt.cla()

    @staticmethod
    def setLegend(ax, has_legend = True, legend_loc = 3, legend_ncol = 1
                  , legend_size = 20, legend_frameon = False):
        if has_legend:
            ax.legend(loc = legend_loc
                      , ncol = legend_ncol
                      , prop = {'size': legend_size}
                      , handletextpad = 0.3
                      , labelspacing = 0.3
                      , columnspacing = 0.3
                      , borderaxespad = 0.3
                      , borderpad = 0.3
                      , frameon = legend_frameon)

    @staticmethod
    def drawList2d(
                list2d = None,
                 header = None,
                 see_col_list = None,
                 save_to_path = None,
                 skip_footer = 0,
                 font_size = 18,
                 linewidth = 3,
                 line_style_list = None,
                 line_marker_list = None,
                 marker_number = 6,
                 line_color_list = None,
                 line_alpha_list = None,
                 xLabel = "",
                 xLabelFontSize = 24,
                 yLabel = "",
                 yLabelFontSize = 24,
                 xLim = None,
                 yLim = None,
                 step_size = None,
                 markeredgewidth = 2,
                 has_legend = True,
                 legend_loc = 4,#'center right',
                 legend_ncol = 1,
                 legend_size = 20,
                 legend_frameon = False,
                 is_sci_notation_in_y_axis = True,
                 csvpath = None
                 ):
        assert csvpath != None or list2d != None
        if csvpath != None:
            list2d = Tools.readCSVAsFloat(csvpath)
            figName = csvpath.replace('.csv', '.png')
            save_to_path = figName

        DrawTools.setFonts(font_size)

        # prepare data to use
        list2d, nrow, ncol = DrawTools.parseList2d(list2d)
        plot_to_row_index = nrow - skip_footer
#         print(nrow, skip_footer, plot_to_row_index)
        x_data = list2d[:plot_to_row_index, 0]

        if see_col_list != None:
            col_list = [see_col for see_col in see_col_list]
        else:
            col_list = [i for i in range(1, ncol)]
        # print(len(col_list))
        assert len(header) == len(col_list) + 1
        # plot to axes
        ax = plt.subplot()
        lines = []
#         print(col_list)
        line_style_list = ['-', '--', '-.', ':']
        for col_index in col_list:
            # first column (index 0) indicates x-axis
            # from 1, a col indicates a y-axis of a feature (e.g. steps in each episode)
            markevery = int(plot_to_row_index / (marker_number))
            ####### styles ########
            linestyle, color, marker, alpha = DrawTools \
                .getPlotPropertiesByListColIndex(col_index
                                      , line_style_list
                                    , line_color_list
                                    , line_marker_list
                                    , line_alpha_list)

            line = ax.plot(x_data, list2d[:plot_to_row_index, col_index],
                            linewidth = linewidth,
                            label = header[col_index],
                            linestyle = linestyle,
                            color = color,
                            marker = marker,
                            markevery = markevery,
                            markersize = 12
                            , markeredgewidth = markeredgewidth
                            , markerfacecolor = 'None'
                            )
            lines.append(line)

        # set legend
        DrawTools.setLegend(ax, has_legend, legend_loc, legend_ncol
                  , legend_size, legend_frameon)

        # set x, y plotting
        if xLim == None:
            xLim = (x_data[0], 300)#x_data[plot_to_row_index - 1]
        plt.xlim(xLim)
        plt.ylim(yLim)
        plt.xlabel('Iterations', fontsize = xLabelFontSize)
        plt.ylabel('Proportion of joint behaviors', fontsize = yLabelFontSize)

        if step_size != None:
            plt.xticks(np.arange(min(x_data), max(x_data) + 1, step_size))

        # set scientific notation
        if is_sci_notation_in_y_axis:
            mf = matplotlib.ticker.ScalarFormatter(useMathText = True)
            mf.set_powerlimits((-2, 2))
            plt.gca().yaxis.set_major_formatter(mf)

        plt.tight_layout()

        # save or plot
        if save_to_path != None:
            DrawTools.saveFig(save_to_path)
        else:
            plt.show()

    @staticmethod
    def drawList3d(
            list2d=None,
            header=None,
            see_col_list=None,
            save_to_path=None,
            skip_footer=0,
            font_size=18,
            linewidth=3,
            line_style_list=None,
            line_marker_list=None,
            marker_number=12,
            line_color_list=None,
            line_alpha_list=None,
            xLabel="",
            xLabelFontSize=24,
            yLabel="",
            yLabelFontSize=24,
            xLim=None,
            yLim=None,
            step_size=None,
            markeredgewidth=2,
            has_legend=True,
            legend_loc=7,#4,
            legend_ncol=1,
            legend_size=20,
            legend_frameon=False,
            is_sci_notation_in_y_axis=True,
            csvpath=None
    ):
        assert csvpath != None or list2d != None
        if csvpath != None:
            list2d = Tools.readCSVAsFloat(csvpath)
            figName = csvpath.replace('.csv', '.png')
            save_to_path = figName

        DrawTools.setFonts(font_size)

        # prepare data to use
        list2d, nrow, ncol = DrawTools.parseList2d(list2d)
        plot_to_row_index = nrow - skip_footer
        #         print(nrow, skip_footer, plot_to_row_index)
        x_data = list2d[:plot_to_row_index, 0]

        if see_col_list != None:
            col_list = [see_col for see_col in see_col_list]
        else:
            col_list = [i for i in range(1, ncol)]
        # print(len(col_list))
        assert len(header) == len(col_list) + 1
        # plot to axes
        ax = plt.subplot()
        lines = []
        #         print(col_list)
        line_style_list = ['-', '--', '-.', ':']
        line_marker_list = ['v', 'o', '*', 'd']
        for col_index in col_list:
            # first column (index 0) indicates x-axis
            # from 1, a col indicates a y-axis of a feature (e.g. steps in each episode)
            markevery = int(plot_to_row_index / (marker_number))
            ####### styles ########
            linestyle, color, marker, alpha = DrawTools \
                .getPlotPropertiesByListColIndex(col_index
                                                 , line_style_list
                                                 , line_color_list
                                                 , line_marker_list
                                                 , line_alpha_list)

            line = ax.plot(x_data, list2d[:plot_to_row_index, col_index],
                           linewidth=linewidth,
                           label=header[col_index],
                           linestyle=linestyle,
                           color=color,
                           marker=marker,
                           markevery=markevery,
                           markersize=12
                           , markeredgewidth=markeredgewidth
                           , markerfacecolor='None'
                           )
            lines.append(line)

        # set legend
        DrawTools.setLegend(ax, has_legend, legend_loc, legend_ncol
                            , legend_size, legend_frameon)

        # set x, y plotting
        if xLim == None:
            xLim = (x_data[0], 300)#x_data[plot_to_row_index - 1])
        plt.xlim(xLim)
        plt.ylim(yLim)
        plt.xlabel('Iterations', fontsize=xLabelFontSize)
        plt.ylabel('Proportion of Emotion', fontsize=yLabelFontSize)

        if step_size != None:
            plt.xticks(np.arange(min(x_data), max(x_data) + 1, step_size))

        # set scientific notation
        if is_sci_notation_in_y_axis:
            mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
            mf.set_powerlimits((-2, 2))
            plt.gca().yaxis.set_major_formatter(mf)

        plt.tight_layout()

        # save or plot
        if save_to_path != None:
            DrawTools.saveFig(save_to_path)
        else:
            plt.show()

    @staticmethod
    def trim(im):
        im = im.convert('RGB')
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    @staticmethod
    def drawNoHeaderCsvWithStyBar(
                 csvpath = None,
                 csv_value = None,
                 x_labels = None,
                 bar_ini_pos_offset = 0,
                 bar_width = 0.15,
                 font_size = 16,
                 legendLableList = None,
                 colorList = None,
                 edgecolorList = None,
                 hatchList = None,
                 alphaList = None,
                 xLabel = "",
                 xLabelFontSize = 22,
                 yLabel = "",
                 yLabelFontSize = 22,
                 notShow = False,
                 figurePath = None,
                 ureWithFileName = True,
                 lengendLoc = 3,
                 usecols = -1,
                 xLim = None,
                 yLim = None,
                 hasLegend = False,
                 legendSize = 20,
                 lgframeon = False,
                 useSciforY = False,
                 figName = None
                 ):
        assert csvpath != None or csv_value != None
        if csvpath != None:
            list2d = Tools.readCSVAsFloat(csvpath)
            figName = csvpath.replace('.csv', '.png')
        else:
            list2d = csv_value
        list2d = np.asarray(list2d)
        nrow = len(list2d)
        ncol = len(list2d[0])
        if len(x_labels) > 0:
            assert len(x_labels) == nrow
#         print list2d
        # bar information
        n_groups = nrow
        bar_ini_pos = np.arange(n_groups)

        matplotlib.rcParams.update({'font.size': font_size})
        matplotlib.rcParams['font.family'] = 'Times New Roman'
#         matplotlib.rcParams['mathtext.fontset'] = 'custom'
        ax = plt.subplot()
        if useSciforY:
            plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0, 0), useMathText = True)
        # first column (index 0) is x-axis, y starts from index 1
        bars = []

        for col_index in range(0, ncol):
            bar_data = list2d[:, col_index]
            ####### styles ########
            if colorList != None:
                color = colorList[col_index]
            else:
                color = None

            if legendLableList != None:
                label = legendLableList[col_index]
            else:
                label = None

            if edgecolorList != None:
                edgecolor = edgecolorList[col_index]
            else:
                edgecolor = None

            if hatchList != None:
                hatch = hatchList[col_index]
            else:
                hatch = None

            if alphaList != None:
                alpha = alphaList[col_index]
            else:
                alpha = None

            bar = ax.bar(bar_ini_pos + bar_ini_pos_offset * bar_width + bar_width * (col_index - 1), bar_data, bar_width,
                            color = color,
                            alpha = alpha,
                            edgecolor = edgecolor,
                            hatch = hatch,
                            label = label
                            )
            bars.append(bar)

        if hasLegend:
            ax.legend(loc = lengendLoc
                      , prop = {'size': legendSize}
                      , handletextpad = 0.3
                      , labelspacing = 0.3
                      , borderaxespad = 0.3
                      , borderpad = 0.3
                      , frameon = lgframeon)

        plt.xticks(bar_ini_pos + bar_width, x_labels)
#         plt.xticks(rotation=45)
        plt.ylim(yLim)
#         plt.gca().invert_xaxis()
        plt.xlabel(xLabel, fontsize = xLabelFontSize)
        plt.ylabel(yLabel, fontsize = yLabelFontSize)

        mf = matplotlib.ticker.ScalarFormatter(useMathText = True)
        mf.set_powerlimits((-2, 2))
        plt.gca().yaxis.set_major_formatter(mf)
        plt.tight_layout()

        if figName != None:
            DrawTools.saveFig(figName)
        else:
            plt.show()

        plt.cla()
