import os, sys

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.sockets.netstat import NetStat

from vyperlogix.os.shell import Shell

__base__ = '/usr/local'
if (_utils.isUsingLinux):
    __base__ = '/usr/local'
elif (_utils.isUsingWindows):
    __base__ = 'J:/@Deployments/'
    
__templates__ = '@@TEMPLATE@@'

__django__ = '_Django-1.3_Multi-Threaded'
__library__ = 'vyperlogix_2_7_0.zip'

__scripts__ = 'scripts'

__app_name_symbol__ = '{{app-name}}'

__dir_name_symbol__ = '{{dir-name}}'

__isUsingLinux__ = _utils.isUsingLinux
__isUsingWindows__ = _utils.isUsingWindows
__isUsingMacOSX__ = _utils.isUsingMacOSX

###########################################################################################################
## Phase I:  (Done !!!)
##           Allocate the directories with symbolic links.  Make the site ready to be uploaded.
##
## Phase II: (50% Done !!!)
##           Allocate the port for the site.  Determine the TCP/IP port.
##           Consumed ports are determined - ready for the port allocation.
##
## Phaese III:
##           Upload the site and perform some sanity checks to ensure the site is ready for use.
##
## Phase IV:
##           Create the nginx site and perform "nginx reload" function to begin using the site.
###########################################################################################################

def shell_callback(data):
    print '%s :: %s' % (misc.funcName(),data)

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
            '--name':'app name.',
            '--netstat':'determine used ports via netstat.',
            '--test':'test a new feature.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName

	_isVerbose = __args__.get_var('isVerbose',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isVerbose=%s' % (_isVerbose)
	_isDebug = __args__.get_var('isDebug',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isDebug=%s' % (_isDebug)
	_isHelp = __args__.get_var('isHelp',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isHelp=%s' % (_isHelp)
	_AppName = __args__.arguments['name']
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _AppName=%s' % (_AppName)
	_isNetstat = __args__.get_var('isNetstat',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isNetstat=%s' % (_isNetstat)
	_isTest = __args__.get_var('isTest',Args._bool_,False)
	if (_isVerbose):
	    print >>sys.stderr, 'DEBUG: _isTest=%s' % (_isTest)

	if (_isHelp):
	    ppArgs()
	    sys.exit()

	if (_isTest):
	    print 'BEGIN: TEST'
	    #s = Shell('dir c:/',callback=shell_callback,isDebugging=True,isWait=True,isExit=False)
	    print 'END!   TEST'
		
	if (_isNetstat):
	    print 'BEGIN: NETSTAT'
	    n = NetStat(isDebugging=True)
	    print '='*40
	    for l in n.listeners:
		print l
	    print '='*40
	    for p in n.ports:
		print '%d' % (p)
	    __port__ = None
	    __ports__ = [p for p in n.ports if (p > 999)]
	    __ports_available__ = set([p for p in xrange(1000,65535)]) - set(__ports__)
	    __preferred__ = [[p for p in xrange(n,n+1000) if (p < 65535)] for n in xrange(8000,65535,1000)]
	    print 'DEBUG:  %s' % ([p for p in __ports_available__ if (p >= 8000) and (p <= 8999)])
	    for port_range in __preferred__:
		print 'DEBUG:  %s --> %s' % (port_range[0],port_range[-1])
		pp = set(__ports_available__) and set(port_range)
		print 'DEBUG:  %s --> %s' % (list(pp)[0:5],list(pp)[-5:])
		if (len(pp) > 0):
		    __port__ = list(pp)[0]
		    break
	    print 'DEBUG:  __port__=%s' % (__port__)
	    print 'END!   NETSTAT'
	
	print 'BEGIN: %s' % (_AppName)
	if (_AppName):
	    ch = os.sep if (not __base__.endswith(os.sep)) and (not __base__.endswith('\\' if (os.sep != '\\') else '/')) else ''
	    fpath = ch.join([__base__,_AppName])
	    if (not os.path.exists(fpath)):
		os.mkdir(fpath)
		templates = ch.join([__base__,__templates__])
		scripts_source = os.sep.join([templates,__scripts__])
		if (os.path.exists(scripts_source)):
		    t_source = os.sep.join([templates,__django__])
		    t_dest = os.sep.join([fpath,__django__])
		    try:
			os.symlink(t_source,t_dest)
		    except:
			print >> sys.stderr, 'WARNING: Cannot make a symbolic link for "%s" --> "%s".' % (t_dest,t_source)
		    t_source = os.sep.join([templates,__library__])
		    t_dest = os.sep.join([fpath,__library__])
		    try:
			os.symlink(t_source,t_dest)
		    except:
			print >> sys.stderr, 'WARNING: Cannot make a symbolic link for "%s" --> "%s".' % (t_dest,t_source)
		    fpath_dest = os.path.dirname(t_dest)
		    files = os.listdir(scripts_source)
		    for f in files:
			fpath = os.sep.join([scripts_source,f])
			fContents = _utils.read_lines_simple(fpath,'rb')
			for i in xrange(0,len(fContents)):
			    fC = fContents[i].replace(__app_name_symbol__,_AppName).replace(__dir_name_symbol__,os.path.dirname(fpath_dest))
			    fContents[i] = fC
			fpath = os.sep.join([fpath_dest,os.path.basename(fpath).replace(__app_name_symbol__,_AppName)])
			print 'Writing... "%s".' % (fpath)
			_utils.writeFileFrom(fpath,'\n'.join(fContents),mode='wb')
		    if (not __isUsingWindows__):
			s = Shell('cd %s; chmod +x *.sh' % (fpath_dest),isWait=True,isExit=False,isDebugging=True)
		else:
		    print 'Rollback --> "%s".' % (fpath)
		    os.rmdir(fpath) # roll it all back !!!
		    print >> sys.stderr, 'WARNING: Cannot proceed without the directory "%s" because this directory is required.' % (scripts_source)
	    else:
		print >> sys.stderr, 'WARNING: Cannot proceed with "%s" because this App Name is already taken.' % (_AppName)
	else:
	    print >> sys.stderr, 'WARNING: Cannot proceed without a valid App Name via the --name="" option.'
	print 'END!  %s' % (_AppName)
