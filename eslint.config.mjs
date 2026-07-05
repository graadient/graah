import tsPlugin from '@typescript-eslint/eslint-plugin'
import tsParser from '@typescript-eslint/parser'
import importPlugin from 'eslint-plugin-import'
import promisePlugin from 'eslint-plugin-promise'
import reactPlugin from 'eslint-plugin-react'
import reactHooksPlugin from 'eslint-plugin-react-hooks'
import simpleImportSort from 'eslint-plugin-simple-import-sort'

const restrictedGlobals = [
    'addEventListener',
    'blur',
    'close',
    'closed',
    'confirm',
    'crypto',
    'defaultStatus',
    'defaultstatus',
    'event',
    'external',
    'fetch',
    'find',
    'focus',
    'frameElement',
    'frames',
    'history',
    'innerHeight',
    'innerWidth',
    'length',
    'location',
    'locationbar',
    'menubar',
    'moveBy',
    'moveTo',
    'name',
    'onblur',
    'onerror',
    'onfocus',
    'onload',
    'onresize',
    'onunload',
    'open',
    'opener',
    'opera',
    'outerHeight',
    'outerWidth',
    'pageXOffset',
    'pageYOffset',
    'parent',
    'print',
    'removeEventListener',
    'resizeBy',
    'resizeTo',
    'screen',
    'screenLeft',
    'screenTop',
    'screenX',
    'screenY',
    'scroll',
    'scrollbars',
    'scrollBy',
    'scrollTo',
    'scrollX',
    'scrollY',
    'self',
    'status',
    'statusbar',
    'stop',
    'toolbar',
    'top',
]

export default [
    {
        ignores: [
            'node_modules/**',
            '.pnp.*',
            '.yarn/**',
            '.expo/**',
            'dist/**',
            'web-build/**',
            'expo-env.d.ts',
            'src/uniwind.d.ts',
        ],
    },
    {
        files: ['**/*.{js,jsx,ts,tsx}'],
        plugins: {
            import: importPlugin,
            'simple-import-sort': simpleImportSort,
            promise: promisePlugin,
            react: reactPlugin,
            'react-hooks': reactHooksPlugin,
        },
        settings: {
            react: { version: 'detect' },
        },
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'module',
            parserOptions: {
                ecmaFeatures: { jsx: true },
            },
        },
        rules: {
            'no-console': 'off',
            'no-unused-vars': 'error',
            eqeqeq: ['warn', 'smart'],
            'no-array-constructor': 'warn',
            'no-caller': 'warn',
            'no-cond-assign': ['warn', 'except-parens'],
            'no-control-regex': 'warn',
            'no-delete-var': 'warn',
            'no-dupe-args': 'warn',
            'no-dupe-class-members': 'warn',
            'no-dupe-keys': 'warn',
            'no-empty': ['error', { allowEmptyCatch: false }],
            'no-empty-character-class': 'warn',
            'no-empty-pattern': 'warn',
            'no-ex-assign': 'warn',
            'no-extend-native': 'warn',
            'no-extra-bind': 'warn',
            'no-extra-label': 'warn',
            'no-func-assign': 'warn',
            'no-implied-eval': 'warn',
            'no-invalid-regexp': 'warn',
            'no-iterator': 'warn',
            'no-label-var': 'warn',
            'no-labels': ['warn', { allowLoop: true, allowSwitch: false }],
            'no-loop-func': 'warn',
            'no-mixed-operators': [
                'warn',
                {
                    groups: [
                        ['&', '|', '^', '~', '<<', '>>', '>>>'],
                        ['==', '!=', '===', '!==', '>', '>=', '<', '<='],
                        ['&&', '||'],
                        ['in', 'instanceof'],
                    ],
                    allowSamePrecedence: false,
                },
            ],
            'no-multi-str': 'warn',
            'no-global-assign': 'warn',
            'no-unsafe-negation': 'warn',
            'no-new-func': 'warn',
            'no-object-constructor': 'warn',
            'no-new-native-nonconstructor': 'warn',
            'no-obj-calls': 'warn',
            'no-octal': 'warn',
            'no-regex-spaces': 'warn',
            'no-script-url': 'warn',
            'no-self-assign': 'warn',
            'no-self-compare': 'warn',
            'no-shadow-restricted-names': 'warn',
            'no-sparse-arrays': 'warn',
            'no-this-before-super': 'warn',
            'no-undef': 'error',
            'no-unreachable': 'warn',
            'no-unused-expressions': [
                'error',
                {
                    allowShortCircuit: true,
                    allowTernary: true,
                    allowTaggedTemplates: true,
                },
            ],
            'no-unused-labels': 'warn',
            'no-useless-computed-key': 'warn',
            'no-useless-rename': [
                'warn',
                {
                    ignoreDestructuring: false,
                    ignoreImport: false,
                    ignoreExport: false,
                },
            ],
            'no-with': 'warn',
            strict: ['warn', 'never'],
            'getter-return': 'warn',
            'no-debugger': 'off',
            'no-unsafe-finally': 'off',
            'default-case': 'off',
            'no-duplicate-case': 'off',
            'no-fallthrough': 'off',
            'no-template-curly-in-string': 'off',
            'no-throw-literal': 'off',
            'no-useless-concat': 'off',
            'no-useless-constructor': 'off',
            'no-useless-escape': 'off',
            'require-yield': 'off',
            'use-isnan': 'off',
            'no-redeclare': 'off',
            'no-sequences': 'off',
            'no-octal-escape': 'off',
            'no-new-wrappers': 'off',
            'no-const-assign': 'off',
            'array-callback-return': 'off',
            'valid-typeof': 'off',
            'no-restricted-globals': ['error', ...restrictedGlobals],
            'no-constant-binary-expression': 'error',
            'no-useless-assignment': 'warn',
            'require-atomic-updates': 'error',
            'react-hooks/rules-of-hooks': 'error',
            'react-hooks/exhaustive-deps': [
                'warn',
                {
                    additionalHooks:
                        '(useAnimatedStyle|useDerivedValue|useAnimatedProps)',
                },
            ],
            'no-restricted-syntax': [
                'error',
                {
                    selector:
                        "CallExpression[callee.name='useEffect'][arguments.length<2]",
                    message:
                        'useEffect must have a dependency array. If the effect does not depend on values, pass [].',
                },
                {
                    selector:
                        "CallExpression[callee.object.name='Object'][callee.property.name='keys']",
                    message:
                        'Avoid Object.keys - it returns string[]. Add/use a type-safe toolkit helper instead.',
                },
                {
                    selector:
                        "CallExpression[callee.object.name='Object'][callee.property.name='values']",
                    message:
                        'Avoid Object.values - it loses key association. Add/use a type-safe toolkit helper instead.',
                },
                'WithStatement',
            ],
            'no-restricted-imports': [
                'error',
                {
                    paths: [
                        {
                            name: 'expo-secure-store',
                            message:
                                'Use toolkit/domain storage wrappers instead of importing expo-secure-store directly.',
                        },
                        {
                            name: 'firebase',
                            message:
                                'Use api/firebase wrappers instead of importing Firebase directly.',
                        },
                        {
                            name: 'firebase/app',
                            message:
                                'Use api/firebase wrappers instead of importing Firebase directly.',
                        },
                        {
                            name: 'lucide-react-native',
                            message:
                                'Use app-ui icon adapters instead of importing lucide-react-native directly.',
                        },
                    ],
                    patterns: [
                        {
                            group: ['@react-native-firebase/*'],
                            message:
                                'Use api/firebase wrappers instead of importing native Firebase directly.',
                        },
                    ],
                },
            ],
            'import/first': 'error',
            'import/no-anonymous-default-export': 'error',
            'import/no-unresolved': 'off',
            'simple-import-sort/imports': [
                'error',
                {
                    groups: [
                        ['^react'],
                        ['^expo', '^@react-navigation'],
                        ['^@heroui', '^heroui-native', '^uniwind'],
                        ['^@/app-ui', '^@/navigation'],
                        ['^@/toolkit'],
                        ['^@/domains'],
                        ['^@/api'],
                        ['^.'],
                        ['^..'],
                    ],
                },
            ],
            'simple-import-sort/exports': 'error',
            'promise/no-return-wrap': 'error',
            'promise/param-names': 'error',
            'promise/no-new-statics': 'error',
            'promise/always-return': 'off',
            'promise/catch-or-return': 'off',
            'react/react-in-jsx-scope': 'off',
            'react/display-name': 'off',
            'react/prop-types': 'off',
            'react/jsx-curly-brace-presence': 'error',
        },
    },
    {
        files: ['**/*.ts', '**/*.tsx'],
        languageOptions: {
            parser: tsParser,
            parserOptions: {
                project: ['./tsconfig.app.json', './tsconfig.node.json'],
                tsconfigRootDir: import.meta.dirname,
            },
        },
        plugins: {
            '@typescript-eslint': tsPlugin,
        },
        rules: {
            'no-unused-vars': 'off',
            'no-undef': 'off',
            '@typescript-eslint/ban-ts-comment': 'off',
            '@typescript-eslint/no-explicit-any': 'off',
            '@typescript-eslint/no-unused-vars': [
                'error',
                {
                    args: 'none',
                    ignoreRestSiblings: true,
                    varsIgnorePattern: '^_',
                    caughtErrors: 'all',
                    caughtErrorsIgnorePattern: '^_',
                },
            ],
            '@typescript-eslint/switch-exhaustiveness-check': 'error',
            '@typescript-eslint/no-floating-promises': 'error',
            '@typescript-eslint/no-misused-promises': [
                'error',
                { checksVoidReturn: { attributes: false } },
            ],
            '@typescript-eslint/await-thenable': 'error',
            '@typescript-eslint/no-unsafe-assignment': 'warn',
            '@typescript-eslint/no-unsafe-return': 'warn',
            '@typescript-eslint/no-unsafe-call': 'warn',
            '@typescript-eslint/no-unsafe-member-access': 'warn',
            '@typescript-eslint/no-unsafe-argument': 'warn',
            '@typescript-eslint/no-misused-spread': 'error',
            '@typescript-eslint/no-empty-object-type': 'error',
            '@typescript-eslint/no-unsafe-function-type': 'error',
            '@typescript-eslint/no-unnecessary-type-parameters': 'warn',
            '@typescript-eslint/no-unnecessary-type-conversion': 'warn',
            '@typescript-eslint/prefer-find': 'warn',
            '@typescript-eslint/unbound-method': 'warn',
            '@typescript-eslint/explicit-function-return-type': [
                'warn',
                {
                    allowExpressions: true,
                    allowTypedFunctionExpressions: true,
                    allowHigherOrderFunctions: true,
                },
            ],
        },
    },
    {
        files: ['**/*.tsx'],
        rules: {
            '@typescript-eslint/explicit-function-return-type': 'off',
        },
    },
    {
        files: ['api/**/*.ts', 'api/**/*.tsx', 'toolkit/Storage/**/*.ts'],
        rules: {
            'no-restricted-imports': 'off',
        },
    },
    {
        files: ['app-ui/icons/**/*.ts', 'app-ui/icons/**/*.tsx'],
        rules: {
            'no-restricted-imports': 'off',
        },
    },
    {
        files: ['api/**/*.ts', 'scripts/**/*.ts'],
        rules: {
            'no-restricted-globals': [
                'error',
                ...restrictedGlobals.filter((g) => g !== 'fetch'),
            ],
        },
    },
    {
        files: ['scripts/**/*.ts'],
        rules: {
            'no-restricted-syntax': 'off',
            '@typescript-eslint/no-unsafe-assignment': 'off',
            '@typescript-eslint/no-unsafe-call': 'off',
            '@typescript-eslint/no-unsafe-member-access': 'off',
            '@typescript-eslint/no-unsafe-argument': 'off',
            '@typescript-eslint/no-unsafe-return': 'off',
            '@typescript-eslint/unbound-method': 'off',
            '@typescript-eslint/explicit-function-return-type': 'off',
        },
    },
    {
        files: [
            '**/*.spec.ts',
            '**/*.spec.tsx',
            '**/*.test.ts',
            '**/*.test.tsx',
        ],
        rules: {
            '@typescript-eslint/await-thenable': 'off',
            '@typescript-eslint/no-floating-promises': 'off',
            '@typescript-eslint/no-unsafe-assignment': 'off',
            '@typescript-eslint/no-unsafe-call': 'off',
            '@typescript-eslint/no-unsafe-member-access': 'off',
            '@typescript-eslint/no-unsafe-return': 'off',
            '@typescript-eslint/no-unsafe-argument': 'off',
            '@typescript-eslint/explicit-function-return-type': 'off',
        },
    },
]
