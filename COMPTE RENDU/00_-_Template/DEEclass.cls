%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% DEE@ISEP class for DEE BSc reports
% original file adapted and further developed by Vitor M. R. Cunha
% % v1.4, Jul 2021
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% original file:
% Masters/Doctoral Thesis 
% Class File
% Version 1.6 (27/8/17)
%
% This class was downloaded from:
% http://www.LaTeXTemplates.com
%
% Authors:
% Vel (vel@latextemplates.com)
% Johannes Böttcher
%
% Notes:
% 1) This class file defines the structure and layout of the template file (main.tex).
% 2) It has been written in such a way that under most circumstances you should not need
% to edit it; updating it to a newer version will be harder. If you do make changes, please change the name of
% the file and add comments to make your changes more visible.
%
% Class license:
% LPPL v1.3c (http://www.latex-project.org/lppl)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%	CLASS DEFINITION AND PARAMETERS
%----------------------------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}[1996/12/01]
\newcommand{\classname}{DEEclass}
\ProvidesClass{\classname}[DEEclass v1.3 DEE@ISEP]
\providecommand{\baseclass}{book}
\RequirePackage{etoolbox}
\RequirePackage{xparse}

\newbool{nolistspace}
\booltrue{nolistspace}	%keeps tables single spaced
\newbool{listtoc}
\booltrue{listtoc}		%add lists to the toc
\newbool{headsepline}
\booltrue{headsepline}	%add header underline
\newbool{portuguese}	%to set the babel language 
\newbool{LEEC}			%to set the DEE course for front pages
\newbool{LETI}

\DeclareOption{portuguese}{\booltrue{portuguese}}
\DeclareOption{LEEC}{\booltrue{LEEC}}
\DeclareOption{LETI}{\booltrue{LETI}}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{\baseclass}}
\ProcessOptions\relax

\LoadClass[11pt,a4paper]{\baseclass}

\newcommand{\poubelle}[1]{}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Simple interface for the user  to customize the chapter titles 
\ProvideDocumentCommand{\abovechapterskip}{}{\vspace*{20pt}}
\ProvideDocumentCommand{\chapterbelowskip}{}{\vspace*{40pt}}
\ProvideDocumentCommand{\chapterinbetweenskip}{}{\vspace*{20pt}}
\ProvideDocumentCommand{\autodot}{}{}
\ProvideDocumentCommand{\mdtChapapp}{}{}
\ProvideDocumentCommand{\chapteralign}{}{\raggedright}
\ProvideDocumentCommand{\chapterfont}{}{\Huge\bfseries}
\ProvideDocumentCommand{\chapterprefixfont}{}{\LARGE\bfseries}

\DeclareDocumentCommand{\@makechapterhead}{ m }{%
	\abovechapterskip
	{\parindent \z@ \chapteralign \normalfont
		\ifnum \c@secnumdepth >\m@ne
		\if@mainmatter{
				\vspace*{100pt}
				\chapterprefixfont \@chapapp\space \thechapter
				\par\nobreak
				\chapterinbetweenskip } 			
		\else {
				\chapterprefixfont \@chapapp\space \thechapter
				\par\nobreak
				\chapterinbetweenskip  	}		
		\fi
		\fi
		\interlinepenalty\@M%
		\chapterfont #1\par\nobreak
		\chapterbelowskip
		\if@mainmatter{		
			\vspace*{40pt}}		
		\fi
	}
	\thispagestyle{\chapter@p@gestyle}
}

\def\@makeschapterhead#1{%
	\abovechapterskip
	{\parindent \z@ \chapteralign
		\normalfont
		\interlinepenalty\@M
		\chapterfont  #1\par\nobreak
		\chapterbelowskip
	}
	\thispagestyle{\chapter@p@gestyle}
}

% Addchap provides unnumbered chapters with an entry in the table of contents as well as an updated header
\ProvideDocumentCommand{\addchap}{ s o m }{%
	\chapter*{#3}%
	\markboth{}{}%
	\IfBooleanTF{#1}{%
	}{%
		\IfNoValueTF{#2}{%
			\addchaptertocentry{#3}%
			\markboth{\MakeMarkcase{#3}}{\MakeMarkcase{#3}}%
		}{%
			\addchaptertocentry{#2}%
			\markboth{\MakeMarkcase{#2}}{\MakeMarkcase{#2}}%
		}%
	}%
}%

\ProvideDocumentCommand{\addsec}{ s o m }{%
	\section*{#3}%
	\markright{}%
	\IfBooleanTF{#1}{%
	}{%
		\IfNoValueTF{#2}{%
			\addcontentsline{toc}{section}{#3}%
			\markright{\MakeMarkcase{#3}}%%
		}{%
			\addcontentsline{toc}{section}{#2}%
			\markright{\MakeMarkcase{#2}}%
		}%
	}%
}%

%----------------------------------------------------------------------------------------
%	CLASS OPTIONS
%----------------------------------------------------------------------------------------

\ifbool{listtoc}{	% With the liststotoc option the lists are added to the table of contents
	\patchcmd{\listoftables}{\@starttoc{lot}}{%
		\addchaptertocentry{\listtablename}\@starttoc{lot}%
	}{}{}%
	\patchcmd{\listoffigures}{\@starttoc{lof}}{%
		\addchaptertocentry{\listfigurename}\@starttoc{lof}%
	}{}{}%
}

\patchcmd{\tableofcontents}{\MakeUppercase}{\MakeMarkcase}{}{}
\patchcmd{\tableofcontents}{\MakeUppercase}{\MakeMarkcase}{}{}
\patchcmd{\listoffigures}{\MakeUppercase}{\MakeMarkcase}{}{}
\patchcmd{\listoffigures}{\MakeUppercase}{\MakeMarkcase}{}{}
\patchcmd{\listoftables}{\MakeUppercase}{\MakeMarkcase}{}{}
\patchcmd{\listoftables}{\MakeUppercase}{\MakeMarkcase}{}{}

%----------------------------------------------------------------------------------------
%	REQUIRED PACKAGES
%----------------------------------------------------------------------------------------
 				
\RequirePackage[utf8]{inputenc} 	% Required for inputting international characters
\RequirePackage[T1]{fontenc} 		% Output font encoding for international characters
\RequirePackage{lmodern} 			% THE font

\ifbool{portuguese}{% Required for automatically changing names of document elements to languages besides english
  \RequirePackage[portuguese]{babel}
	}{
  \RequirePackage[english]{babel}
}

\RequirePackage{scrbase} % Required for handling language-dependent names of sections/document elements

\RequirePackage{scrhack} % Loads fixes for various packages

\RequirePackage{longtable} % Required for tables that span multiple pages 

\RequirePackage{xcolor} % Required for specifying custom colours
\definecolor{lightgray}{rgb}{.9,.9,.9}

\RequirePackage{graphicx} % Required to include images

\graphicspath{{figures/}{front/}} 	% Specifies where to look for included images

\RequirePackage{booktabs} % Required for better table rules

\RequirePackage{caption} % Required for customising the captions
\captionsetup{justification=centerlast,font=small,margin=50pt}

\RequirePackage[autostyle=true]{csquotes} 	% For language-dependent quotes

\RequirePackage[hidelinks]{hyperref}		%To pro­duce hy­per­text links in the doc­u­ment
\hypersetup{hidelinks,
bookmarksopen=true,
bookmarksopenlevel=0,
breaklinks=true,
}
\PassOptionsToPackage{hyphens}{url}\usepackage{hyperref} % To break long urls

\RequirePackage{calc}			% to perform arithmetic on the arguments of the LATEX commands

\RequirePackage{listings} % Required for code listings
\lstset{ %
 %language=C,                        % choose the language of the code
 basicstyle=\footnotesize\ttfamily,
 keywordstyle=\bfseries,
 numbers=left,                      % where to put the line-numbers   
 numberstyle=\tiny\color{gray},		% the size of the fonts that are used for the line-numbers
 stepnumber=1,                      % the step between two line-numbers. If it's 1 each line will be numbered
 numbersep=8pt,                     % how far the line-numbers are from the code
 xleftmargin=2em,					% keep line numbers inside the margins		
 frame=tb,							% frame: top and bottom lines
 framexleftmargin=1.5em,			% frame: adjusts left margin because the xleftmargin numbers setting
 float=!htb,						% if float defined, let Latex manage it
 aboveskip=8mm,
 belowskip=4mm,
 backgroundcolor=\color{white},
 commentstyle=\color{darkgray},    	% comment style
 %keywordstyle=\color{blue},       	% keyword style
 showspaces=false,                  % show spaces adding particular underscores
 showstringspaces=false,            % underline spaces within strings
 showtabs=false,                    % show tabs within strings adding particular underscores
 tabsize=2,	                    	% sets default tabsize to 2 spaces
 captionpos=b,                      % sets the caption-position to bottom
 breaklines=true,                   % sets automatic line breaking
 breakatwhitespace=false,           % sets if automatic breaks should only happen at whitespace
 escapeinside={\%*}{*)},            % if you want to add a comment within your code
 morekeywords={*,var,template,new}  % if you want to add more keywords to the set
}

\RequirePackage[calc,portuguese]{datetime2}	% For date format
\DTMnewdatestyle{mydateformat}{%
  \renewcommand{\DTMdisplaydate}[4]{%
%    \DTMshortweekdayname{##4},\space% 
    \DTMmonthname{##2},\nobreakspace%  
%    \number##3,\space%                
    \number##1%                       
  }%
  \renewcommand{\DTMDisplaydate}{\DTMdisplaydate}%
}

\RequirePackage{siunitx} 		% required for \SI commands
\RequirePackage[acronym,toc,shortcuts,nopostdot,nogroupskip,automake]{glossaries} %for lists of terms, acronyms and symbols
\RequirePackage{enumitem} 		% for acronyms list spacing

\RequirePackage{notoccite}		% prevents cite command count in frontmatter

\RequirePackage[titletoc,title]{appendix} %for easy appendix management

%----------------------------------------------------------------------------------------
%	DEFINE CUSTOM THESIS INFORMATION COMMANDS
%----------------------------------------------------------------------------------------

\NewDocumentCommand{\reporttitle} { o m }{%
 \IfValueTF{#1}{\def\shorttitle{#1}}{\def\shorttitle{#2}}%
 \def\@title{#2}%
 \def\ttitle{#2}%
}
\NewDocumentCommand{\reportsubtitle}{m}{\newcommand{\rsubtitle}{#1}}
\DeclareDocumentCommand{\author}{m}{\newcommand{\authorname}{#1}\renewcommand{\@author}{#1}}
\NewDocumentCommand{\studentnumber}{m}{\newcommand{\stdnumber}{#1}}
\NewDocumentCommand{\studentemail}{m}{\newcommand{\stdemail}{#1}}
\NewDocumentCommand{\advisor}{m m}{\newcommand{\advname}{#1, \url{#2}}}
\NewDocumentCommand{\coadvisor}{m m}{\newcommand{\coadvname}{#1, \url{#2}}}
\NewDocumentCommand{\company}{m}{\newcommand{\companyname}{#1}}
\NewDocumentCommand{\supervisor}{m m}{\newcommand{\supname}{#1, \url{#2}}}
\NewDocumentCommand{\subdate}{m}{\newcommand{\datename}{#1}}
\NewDocumentCommand{\researchgroup}{m}{\newcommand{\groupname}{#1}}

% New command to move content to the next page which prints to the next odd page if twosided mode is active
\newcommand{\checktoopen}{  
	\if@openright\cleardoublepage\else\clearpage\fi
	\ifdef{\phantomsection}{\phantomsection}{}% The \phantomsection command is necessary for hyperref to jump to the correct page
}

\NewDocumentCommand{\bhrule}{}{\typeout{--------------------}}
\NewDocumentCommand{\tttypeout}{m}{\bhrule\typeout{\space #1}\bhrule}

\newcommand{\HRule}{\rule{.9\linewidth}{.6pt}} % New command to make the lines in the title page
\newcommand{\decoRule}{\rule{.8\textwidth}{.4pt}} % New command for a rule to be used under figures
\newcommand{\HRuleFront}{\rule{.98\textwidth}{.3pt}} % New command to make the lines in the title page

\setcounter{tocdepth}{3} % The depth to which the document sections are printed to the table of contents

\ProvideDocumentCommand{\addchaptertocentry}{ m }{%
	\addcontentsline{toc}{chapter}{#1}%
}

\newcommand{\textbetweenrules}[2][.3pt]{%
  \par\vspace{\topsep}
  \noindent\makebox[0.98\textwidth]{%
    \sbox0{#2}%
    \dimen0=.5\dimexpr\ht0+#1\relax
    \dimen2=-.5\dimexpr\ht0-#1\relax
    \leaders\hrule height \dimen0 depth \dimen2\hfill
    \quad #2\quad
    \leaders\hrule height \dimen0 depth \dimen2\hfill
  }\par\nopagebreak\vspace{\topsep}
}

%----------------------------------------------------------------------------------------
%	CUSTOM LANGUAGE SETTINGS
%----------------------------------------------------------------------------------------
\addto{\captionsportuguese}{\renewcommand*\contentsname{\'{I}ndice}}

\addto{\captionsportuguese}{\renewcommand{\appendixname}{Anexo}}

\addto{\captionsenglish}{\renewcommand{\bibname}{References}}
\addto{\captionsportuguese}{\renewcommand{\bibname}{Refer\^{e}ncias}}

\newcommand{\reftocname}{References}
\providecaptionname{english}{\reftocname}{References}
\providecaptionname{portuguese}{\reftocname}{Refer\^{e}ncias}

\addto{\captionsenglish}{\renewcommand{\lstlistlistingname}{Listings}}
\addto{\captionsportuguese}{\renewcommand{\lstlistlistingname}{Listagens}}

\newcommand{\secondLang}{portuguese}
\iflanguage{portuguese}{
	\renewcommand{\lstlistingname}{Listagem}	
	\renewcommand{\secondLang}{english}
	\newtheorem{theorem}{Teorema}
	\newtheorem{corollary}{Corolário}
	\newtheorem{lemma}{Lema}	
}{
	\newtheorem{theorem}{Theorem}
	\newtheorem{corollary}{Corollary}
	\newtheorem{lemma}{Lemma}
}

\RequirePackage[hyperpageref]{backref}
\renewcommand*{\backref}[1]{}
\iflanguage{portuguese}{
    \renewcommand*{\backrefalt}[4]{%
      \ifcase #1 %
      \or
      {\footnotesize [Citado na p\'{a}gina #2]}%
      \else
      {\footnotesize [Citado nas p\'{a}ginas #2]}%
      \fi
    }
    \renewcommand*{\backreftwosep}{ e~}
    \renewcommand*{\backreflastsep}{ e~}
}{
    \renewcommand*{\backrefalt}[4]{%
      \ifcase #1 %
      \or
      {\footnotesize [Cited on page #2]}%
      \else
      {\footnotesize [Cited on pages #2]}%
      \fi
    }
}

%----------------------------------------------------------------------------------------
%	MARGINS and SPACING
%----------------------------------------------------------------------------------------

\RequirePackage{setspace} % Required for changing line spacing
\onehalfspacing	%from the setspace package

\RequirePackage{geometry}
\geometry{
	headheight=4ex,
%	includehead,
%	includefoot,
	paper=a4paper, 
	inner=3cm, % Inner margin
	outer=3.5cm, % Outer margin
	bindingoffset=.5cm, % Binding offset
	top=3.5cm, % Top margin
	bottom=3cm, % Bottom margin
	%showframe, % Uncomment to show how the type block is set on the page	
}

\raggedbottom

% If the option `nolistspacing' is given, the spacing in the different lists is reduced to single spacing. This option is only useful, if the spacing of the document has been changed to onehalfspacing or doublespacing.
\ifbool{nolistspace}{
	\patchcmd{\listoffigures}{%
		\@starttoc{lof}
	}{%
		\begingroup%
		\singlespace\@starttoc{lof}\endgroup%
	}{}{}%
	\patchcmd{\listoftables}{%
		\@starttoc{lot}
	}{%
		\begingroup%
		\singlespace\@starttoc{lot}\endgroup%
	}{}{}%
	\patchcmd{\tableofcontents}{%
		\@starttoc{toc}
	}{%
		\begingroup%
		\singlespace\@starttoc{toc}\endgroup%
	}{}{}%
}{}
%----------------------------------------------------------------------------------------
%	PENALTIES
%----------------------------------------------------------------------------------------

\doublehyphendemerits=10000 % No consecutive line hyphens
\brokenpenalty=10000 % No broken words across columns/pages
\widowpenalty=9999 % Almost no widows at bottom of page
\clubpenalty=9999 % Almost no orphans at top of page
\interfootnotelinepenalty=9999 % Almost never break footnotes

%----------------------------------------------------------------------------------------
%	HEADERS AND FOOTERS STYLE
%----------------------------------------------------------------------------------------

\RequirePackage[markcase=used]{scrlayer-scrpage}
\providepairofpagestyles{thesisSimple}{%
	\clearpairofpagestyles%
	\automark[chapter]{chapter}
	\ihead{\headmark}% Inner header
	\ohead{\pagemark}% Outer header
	\cfoot[\pagemark]{} %new
}
\ifoot{}% Inner footer
\ofoot{}% Outer footer
\pagestyle{thesisSimple}
\providepairofpagestyles[thesisSimple]{thesis}{%
	\automark*[section]{}%
}
\providepairofpagestyles[thesisSimple]{review}{%
	\ofoot[\shorttitle/\authorname]{\shorttitle/\authorname}
	\ifoot[\today]{\today}
}
\pagestyle{thesis}
\ifbool{headsepline}{\KOMAoption{headsepline}{true}}{}
\PreventPackageFromLoading[\ClassError{\classname}{Package `fancyhdr' is
incompatible\MessageBreak with this class}{The pagesyles are defined 
	using package `scrlayer-scrpage', please consult the\MessageBreak 
KOMA-script documentation for details.}]{fancyhdr}

\newcommand{\blank@p@gestyle}{empty}
\newcommand{\chapter@p@gestyle}{plain}
\NewDocumentCommand{\blankpagestyle}{ m }{%
	\ClassWarning{\classname}{\string\blankpagestyle\space is
	obsolete,\MessageBreak use \string\setblankpagestyle \space  instead}\renewcommand{\blank@p@gestyle}{}{#1}
}
\NewDocumentCommand{\setblankpagestyle}{ m }{\renewcommand{\blank@p@gestyle}{#1}}
\NewDocumentCommand{\setchapterpagestyle}{ m }{\renewcommand{\chapter@p@gestyle}{#1}}

\DeclareDocumentCommand\cleardoublepage{}{\clearpage\if@twoside \ifodd\c@page\else
	\hbox{}
	\thispagestyle{\blank@p@gestyle}
	\newpage
	\if@twocolumn\hbox{}\newpage\fi\fi\fi%
}

%----------------------------------------------------------------------------------------
%	TITLE PAGES DESIGN
%----------------------------------------------------------------------------------------

\newcommand{\university}{}
\newcommand{\school}{BEYOND THE SEA}
\newcommand{\department}{}
\newcommand{\degree}{}
\newcommand{\frontcourselabel}{}
\newcommand{\aftercourselabel}{}
\newcommand{\degreeacrn}{}

%BSc
\newcommand{\degreetemp}{}
\newcommand{\disclamertemp}{}

\ifbool{LEEC}{
	\renewcommand{\degreeacrn}{Rapport}
	\renewcommand{\degreetemp}{Rapport}
	\providecaptionname{english}{\degreetemp}{}
	\providecaptionname{portuguese}{\degreetemp}{Stage de césure}
	\renewcommand{\frontcourselabel}{{\large \degreetemp}\\}
	\renewcommand{\disclamertemp}{
            \begin{multicols}{2}
            Author : Romain Lambert
            \columnbreak
            
            Supervisor : Corentin Tran
            \end{multicols}
            }
        \renewcommand{\aftercourselabel}{\large \textit{\disclamertemp \degreetemp}\\}			
}{}

\ifbool{LETI}{
	\renewcommand{\degreeacrn}{LETI}
	\renewcommand{\degreetemp}{Licenciatura em Engenharia de Telecomunicações e Informática}
	\providecaptionname{english}{\degreetemp}{Degree in Telecommunications and Informatics Engineering}
	\providecaptionname{portuguese}{\degreetemp}{Licenciatura em Engenharia de Telecomunicações e Informática}
	\renewcommand{\frontcourselabel}{{\large \degreetemp}\\}
	\renewcommand{\disclamertemp}{This report partially satisfies the requirements defined for the Project/Internship course, in the 3\textsuperscript{rd} year, of the }
	\providecaptionname{english}{\disclamertemp}{This report partially satisfies the requirements defined for the Project/Internship course, in the 3\textsuperscript{rd} year, of the }
	\providecaptionname{portuguese}{\disclamertemp}{Este relat\'{o}rio satisfaz, parcialmente, os requisitos que constam da Ficha de Unidade Curricular de Projeto/Est\'{a}gio, do 3º ano, da }
	\renewcommand{\aftercourselabel}{\large \textit{\disclamertemp \degreetemp.}\\}	
}{}

%%common
\newcommand{\studentlabel}{Candidate}
\providecaptionname{english}{\studentlabel}{Candidate}
\providecaptionname{portuguese}{\studentlabel}{Candidato}

\newcommand{\nblabel}{nb.}
\providecaptionname{english}{\nblabel}{{No. }}
\providecaptionname{portuguese}{\nblabel}{{Nº }}

\newcommand{\advisorlabel}{Scientific Guidance}
\providecaptionname{english}{\advisorlabel}{Scientific Guidance}
\providecaptionname{portuguese}{\advisorlabel}{Orienta\c{c}\~{a}o Cient\'{i}fica}

\newcommand{\coadvisorlabel}{Scientific Co-Guidance}
\providecaptionname{english}{\coadvisorlabel}{Scientific Co-Guidance}
\providecaptionname{portuguese}{\coadvisorlabel}{Coorienta\c{c}\~{a}o Cient\'{i}fica}

\newcommand{\supervisorlabel}{Advisor}
\providecaptionname{english}{\supervisorlabel}{Advisor}
\providecaptionname{portuguese}{\supervisorlabel}{Orientador}

\newcommand{\companylabel}{Company}
\providecaptionname{english}{\companylabel}{Company}
\providecaptionname{portuguese}{\companylabel}{Empresa}


%%1st page
\newcommand{\printcoverpage}{
	\begin{titlepage}
	    \begin{center}
	        % Université et École
	        {\scshape\normalsize \university}\par\vspace{3mm}
	        {\scshape\LARGE \school}\par
	        \HRuleFront
	        \vfill		 
	        
	        % Titre principal
	        {\huge \bfseries \ttitle\par}\vspace{0.4cm} 
	        
	        % Sous-titre conditionnel
	        \ifdefined\rsubtitle 
	            {\large \bfseries \rsubtitle\par\vspace{0.3cm}}
	        \fi
	        
	        \vfill
	        
	        % Auteur
	        {\Large \bfseries \authorname}\par	
	        
	        \vfill
	        
	        % Informations académiques
	        \textbetweenrules[.3pt]{\degreeacrn}\par
	        \vspace{1pt}
	        
	        \vfill	
	        
	        % Logo(s)
	        \includegraphics[width=\textwidth]{Pics/Beyond the sea.png}\par\vspace{1cm}
	        
	        \vspace{3cm}
	        
	        % Date conditionnelle
	        \DTMsetdatestyle{mydateformat}
	        \ifdefined\datename
	            {\normalsize \datename\par\vspace{5mm}}
	        \else
	            {\normalsize \today\par\vspace{5mm}}
	        \fi
	    \end{center}
	\end{titlepage}
}


%----------------------------------------------------------------------------------------
%	MAIN PAGE DESIGN
%----------------------------------------------------------------------------------------

\newcommand{\abstraclabel}{Main}
\providecaptionname{english}{\abstraclabel}{Introduction}
\providecaptionname{portuguese}{\abstraclabel}{Resumo} % Portuguese 

\newenvironment{main}{
	\setcounter{page}{1}
	\checktoopen	
	\tttypeout{\abstraclabel}
	\thispagestyle{plain}
	%\chapter*{\abstraclabel}
	\pdfbookmark[0]{\abstraclabel}{abstract1}	
	}
	{
  	\vfill\null
	}

\newenvironment{secondlangabstract}{
	\checktoopen
	\begin{otherlanguage}{\secondLang}
	\tttypeout{\abstraclabel}
	\thispagestyle{plain}
	\chapter*{\abstraclabel}
	\pdfbookmark[0]{\abstraclabel}{abstract2}
	}
	{
	\end{otherlanguage}
  	\vfill\null
	}

%----------------------------------------------------------------------------------------
%	CUSTOM DISSERTATION COMMANDS
%----------------------------------------------------------------------------------------
% new command for inline graphics (set to line height)
\newlength\myheight				
\newlength\mydepth
\settototalheight\myheight{Xygp}
\settodepth\mydepth{Xygp}
\setlength\fboxsep{0pt}
\newcommand*\inlinegraphics[1]{%
  \settototalheight\myheight{Xygp}%
  \settodepth\mydepth{Xygp}%
  \raisebox{-\mydepth}{\includegraphics[height=\myheight]{#1}}%
}

% Print the bibliographic references using the IEEEtrans format
\newcommand{\printreferences}[1]{
\phantomsection
\addcontentsline{toc}{chapter}{\reftocname}
%\nocite{*}
\bibliographystyle{ieeetr}
\bibliography{#1}
}

% Define some commands to keep the formatting separated from the content 
\newcommand{\tabhead}[1]{\textbf{#1}}
\newcommand{\code}[1]{\texttt{#1}}
%\newcommand{\file}[1]{\texttt{\bfseries#1}}
\newcommand{\file}[1]{\texttt{#1}}
\newcommand{\option}[1]{\texttt{\itshape#1}}

%----------------------------------------------------------------------------------------
\endinput

