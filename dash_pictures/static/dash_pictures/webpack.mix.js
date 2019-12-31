const mix = require('laravel-mix');

mix.js('js/index.js', 'public/app.js')
    .options({
        processCssUrls: false
    });
