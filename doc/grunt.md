# Javascript build

FreedomSponsors development environment uses [grunt](http://gruntjs.com/) to generate a single .js file by concatenating other files.
Basically it will read some files from `djangoproject/statfiles/static/js/**` and write to 'djangoproject/statfiles/static/js-generated/fs.js'.

So anytime you change any javascript, you need to rebuild fs.js

## How to do it

### 1 Install nodejs, npm, and grunt on your operating system

```bash
sudo apt-get install nodejs npm
sudo npm install grunt-cli -g
```
You do this once in a lifetime.

### 2 Download FreedomSponsors node dependencies

```
cd djangoproject
npm install
```

This will create a `node_modules` folder. 
You only need to run `npm install` again if there's any change to the `package.json` file

### 3 Update fs.js

```
cd djangoproject
grunt build
```
You need to run `grunt build` whenever you change anything in the javascript code
