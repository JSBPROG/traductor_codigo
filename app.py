import streamlit as st
import ia 
ia.logging()
languages = [
    "abap", "abnf", "actionscript", "ada", "agda", "al", "antlr4", "apacheconf", "apex", "apl",
    "applescript", "aql", "arduino", "arff", "asciidoc", "asm6502", "asmatmel", "aspnet",
    "autohotkey", "autoit", "avisynth", "avroIdl", "bash", "basic", "batch", "bbcode", "bicep",
    "birb", "bison", "bnf", "brainfuck", "brightscript", "bro", "bsl", "c", "cfscript",
    "chaiscript", "cil", "clike", "clojure", "cmake", "cobol", "coffeescript", "concurnas", "coq",
    "cpp", "crystal", "csharp", "cshtml", "csp", "cssExtras", "css", "csv", "cypher", "d", "dart",
    "dataweave", "dax", "dhall", "diff", "django", "dnsZoneFile", "docker", "dot", "ebnf",
    "editorconfig", "eiffel", "ejs", "elixir", "elm", "erb", "erlang", "etlua", "excelFormula",
    "factor", "falselang", "firestoreSecurityRules", "flow", "fortran", "fsharp", "ftl", "gap",
    "gcode", "gdscript", "gedcom", "gherkin", "git", "glsl", "gml", "gn", "goModule", "go",
    "graphql", "groovy", "haml", "handlebars", "haskell", "haxe", "hcl", "hlsl", "hoon", "hpkp",
    "hsts", "http", "ichigojam", "icon", "icuMessageFormat", "idris", "iecst", "ignore", "inform7",
    "ini", "io", "j", "java", "javadoc", "javadoclike", "javascript", "javastacktrace", "jexl",
    "jolie", "jq", "jsExtras", "jsTemplates", "jsdoc", "json", "json5", "jsonp", "jsstacktrace",
    "jsx", "julia", "keepalived", "keyman", "kotlin", "kumir", "kusto", "latex", "latte", "less",
    "lilypond", "liquid", "lisp", "livescript", "llvm", "log", "lolcode", "lua", "magma",
    "makefile", "markdown", "markupTemplating", "markup", "matlab", "maxscript", "mel", "mermaid",
    "mizar", "mongodb", "monkey", "moonscript", "n1ql", "n4js", "nand2tetrisHdl", "naniscript",
    "nasm", "neon", "nevod", "nginx", "nim", "nix", "nsis", "objectivec", "ocaml", "opencl",
    "openqasm", "oz", "parigp", "parser", "pascal", "pascaligo", "pcaxis", "peoplecode", "perl",
    "phpExtras", "php", "phpdoc", "plsql", "powerquery", "powershell", "processing", "prolog",
    "promql", "properties", "protobuf", "psl", "pug", "puppet", "pure", "purebasic", "purescript",
    "python", "q", "qml", "qore", "qsharp", "r", "racket", "reason", "regex", "rego", "renpy",
    "rest", "rip", "roboconf", "robotframework", "ruby", "rust", "sas", "sass", "scala", "scheme",
    "scss", "shellSession", "smali", "smalltalk", "smarty", "sml", "solidity", "solutionFile",
    "soy", "sparql", "splunkSpl", "sqf", "sql", "squirrel", "stan", "stylus", "swift", "systemd",
    "t4Cs", "t4Templating", "t4Vb", "tap", "tcl", "textile", "toml", "tremor", "tsx", "tt2",
    "turtle", "twig", "typescript", "typoscript", "unrealscript", "uorazor", "uri", "v", "vala",
    "vbnet", "velocity", "verilog", "vhdl", "vim", "visualBasic", "warpscript", "wasm", "webIdl",
    "wiki", "wolfram", "wren", "xeora", "xmlDoc", "xojo", "xquery", "yaml", "yang", "zig"
]

def busca_lenguaje(busqueda: str) -> list[str]:
    return [nombre for nombre in languages if busqueda.lower() in nombre.lower()]

st.title("TRADUCTOR DE CÓDIGO CON IA")
col1, col2= st.columns(2)

with col1:
    st.header("Escribe tu código")
    busqueda = st.text_input("Filtrar lenguajes")  

    user_text = st.text_input(
        "Escribe aquí en python",
        value="",
            max_chars=None,
                key="input_user",
                    type="default",
                        help=None,
                            autocomplete=None,
                                on_change=None,
                                    args=None,
                                        kwargs=None,
                                            placeholder=None,
                                                disabled=False,
                                                    label_visibility="visible",
       
    )

    if st.session_state.input_user:
        st.button("Enviar", key="enviar")

with col2:
    st.header("Respuesta de la IA")
    resultados = busca_lenguaje(busqueda) if busqueda else []

    opcion = st.selectbox(
        "Selecciona el lenguaje coincidente",
        resultados if resultados else ["(No hay resultados)"],
        disabled=not busqueda  
    )

    ia_response = None
    if "enviar" in st.session_state and st.session_state.enviar:  
        ia_response = ia.model_ussage(user_text,opcion)

    if ia_response is not None and opcion:
        st.code(
            ia_response,
            language=opcion,
            line_numbers=True,
            wrap_lines=False,
        )
    

