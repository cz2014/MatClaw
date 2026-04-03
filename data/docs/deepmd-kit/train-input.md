# Training Parameters

Note

One can load, modify, and export the input file by using our effective
web-based tool
[DP-GUI](https://dpgui.deepmodeling.com/input/deepmd-kit-2.0) online or
hosted using the `command line interface <cli>`{.interpreted-text
role="ref"} `dp gui`. All training parameters below can be set in
DP-GUI. By clicking \"SAVE JSON\", one can download the input file for
further training.

Note

One can benefit from IntelliSense and validation when
`writing JSON files using Visual Studio Code <json_vscode>`{.interpreted-text
role="ref"}. See `here <json_vscode>`{.interpreted-text role="ref"} to
learn how to configure.


## Writing JSON files using Visual Studio Code {#json_vscode}

When writing JSON files using [Visual Studio
Code](https://code.visualstudio.com/), one can benefit from IntelliSense
and validation by adding a [JSON schema](https://json-schema.org/). To
do so, in a VS Code workspace, one can generate a JSON schema file for
the input file by running the following command:

``` bash
dp doc-train-input --out-type json_schema > deepmd.json
```

Then one can [map the
schema](https://code.visualstudio.com/docs/languages/json#_mapping-to-a-schema-in-the-workspace)
by updating the workspace settings in the
[.vscode/settings.json]{.title-ref} file as follows:

``` json
{
   "json.schemas": [
      {
            "fileMatch": [
               "/**/*.json"
            ],
            "url": "./deepmd.json"
      }
   ]
}
```
