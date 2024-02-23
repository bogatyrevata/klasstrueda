import gulp from 'gulp';
import autoprefixer from 'autoprefixer';
import browser from 'browser-sync';
import cheerio from 'gulp-cheerio';
import csso from 'postcss-csso';
import data from 'gulp-data';
import { deleteSync } from 'del';
import esbuild from 'gulp-esbuild';
import fs from 'fs';
import notify from 'gulp-notify';
import plumber from 'gulp-plumber';
import postcss from 'gulp-postcss';
import rename from 'gulp-rename';
import render from 'gulp-nunjucks-render';
import sass from 'gulp-dart-sass';
import sharpOptimizeImages from 'gulp-sharp-optimize-images';
import svgmin from 'gulp-svgmin';
import svgstore from 'gulp-svgstore';
const { src, dest, watch, parallel, series } = gulp;

/**
 * Пути к файлам
 */
const path = {
  styles: {
    root: 'app/sass/',
    compile: 'app/sass/style.scss',
    save: 'app/static/css/',
  },
  scripts: {
    root: 'app/static/mjs/script.js',
    save: 'app/static/js/',
  },
  templates: {
    root: 'app/templates/'
  },
  vendor: {
    styles: 'app/vendor/css/',
    scripts: 'app/vendor/js/',
  }
};

/**
 * Основные задачи
 */
export const styles = () => src(path.styles.compile, { sourcemaps: true })
  .pipe(plumber(notify.onError({
    title: 'SCSS',
    message: 'Error: <%= error.message %>'
  })))
  .pipe(sass.sync().on('error', sass.logError))
  .pipe(postcss([
    autoprefixer(),
    csso()
  ]))
  .pipe(rename({
    suffix: `.min`
  }))
  .pipe(dest(path.styles.save, { sourcemaps: '.' }));

export const scripts = () => src(path.scripts.root)
  .pipe(plumber(notify.onError({
    title: 'SCRIPTS',
    message: 'Error: <%= error.message %>'
  })))
  .pipe(esbuild({
    outfile: 'script.min.js',
    bundle: true,
    minify: true,
    sourcemap: 'both'
  }))
  .pipe(dest(path.scripts.save));

export const vendorStyles = () => src(`${path.vendor.styles}*.min.css`)
  .pipe(dest(`${path.styles.save}`))

const vendorScripts = () => src(`${path.vendor.scripts}*.min.js`)
  .pipe(dest(`${path.scripts.save}`))

export const vendor = parallel(vendorStyles, vendorScripts);

export const server = () => {
  const bs = browser.init({
    proxy: '127.0.0.1:5000',
    cors: true,
    notify: false,
    ui: false,
    open: false,
    scrollThrottle: 100,
  });
  watch(`${path.styles.root}**/*.scss`, styles).on('change', bs.reload);
  watch(`${path.scripts.root}**/*.js`, scripts).on('change', bs.reload);
  watch(`${path.templates.root}**/*.j2`).on('change', bs.reload);
};

/**
 * Для билда
 */
export const build = parallel(styles, scripts, vendor);

/**
 * Задачи для разработки
 */
export const start = series(build, server);

export default start;
