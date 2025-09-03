# Troubleshooting Guide

## Common Issues and Solutions

### Chrome Extension Not Loading
**Problem**: The numbered tabs extension isn't appearing in Chrome.

**Solutions**:
1. Check that Developer Mode is enabled in `chrome://extensions/`
2. Verify the `chrome.css` file is properly formatted
3. Reload the extension after making changes
4. Clear browser cache and restart Chrome

### API Connection Issues
**Problem**: Backend API returning 500 errors.

**Solutions**:
- Check server logs for detailed error messages
- Verify all required dependencies are installed
- Ensure database connections are properly configured
- Test API endpoints individually with curl or Postman

### Tab Numbering Not Working
**Problem**: Tab numbers aren't displaying correctly.

**Possible Causes**:
- CSS conflicts with other extensions
- JavaScript execution blocked by browser security
- Outdated browser version

**Steps to Debug**:
1. Open browser developer tools
2. Check console for JavaScript errors
3. Inspect tab elements for CSS application
4. Test in incognito mode to isolate extension conflicts

## Getting Help

For additional support:
- Check existing GitHub issues
- Review the development notes
- Contact the development team
