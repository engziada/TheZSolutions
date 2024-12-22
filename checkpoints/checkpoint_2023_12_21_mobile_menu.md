# Checkpoint: Mobile Menu and Scroll Adjustments
Date: 2023-12-21
Commit: 5e25ece

## Changes Made
1. Added mobile menu functionality:
   - Responsive menu that shows on screens <= 1080px
   - Burger menu button with toggle functionality
   - Proper styling and transitions
   - Menu closes when clicking outside or on a link

2. Fixed scroll offset for sections:
   - Adjusted scroll position to account for logo height
   - Added proper padding to avoid content overlap
   - Improved smooth scrolling behavior

3. Updated mobile layout:
   - Logo moves to left side on mobile
   - Slogan hides on mobile
   - Menu items stack vertically in dropdown

## Files Modified
- app/templates/base.html
- app/static/css/menu.css
- app/forms/contact.py
- app/models/contact.py
- app/routes/main.py
- app/static/css/main.css
- app/templates/main/home.html

## New Files
- app/static/img/circle.svg
- app/static/img/z.svg

## Restore Command
```bash
git checkout 5e25ece
```
