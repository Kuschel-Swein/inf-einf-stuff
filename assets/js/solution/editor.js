export function createEditor({
    element,
    options: { language, value, readOnly },
    buildRevision,
    librarySource,
}) {
    require.config({
        urlArgs: `v=${buildRevision}`,
        paths: {
            vs: librarySource,
        },
    });

    return new Promise(resolve => {
        // use requirejs for monaco compat
        require(['vs/editor/editor.main'], () => {
            const editor = monaco.editor.create(element, {
                language,
                value,
                lineNumbers: 'on',
                automaticLayout: true,
                scrollBeyondLastLine: false,
                renderValidationDecorations: 'on',
                theme: matchMedia('(prefers-color-scheme: dark)').matches
                    ? 'vs-dark'
                    : 'vs-light',
                readOnlyMessage: { value: 'Cannot edit this file.' },
                readOnly,
            });

            resolve([editor, monaco]);
        });
    });
}
