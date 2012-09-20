from django.core.management.base import NoArgsCommand
from optparse import make_option
from core.models import *
from core.utils.frespo_utils import get_or_none
from django.contrib.auth.models import User



def frespoUser():
	user = get_or_none(User, username='freedomsponsors')
	if(user):
		return user
	else:
		user = User()
		user.username = 'freedomsponsors'
		user.email = 'freedomsponsors@freedomsponsors.com'
		user.first_name = 'Freedom'
		user.last_name = 'Sponsors'
		user.save()
	return user

def add_initial_projects():
	frespo_user = frespoUser()
	def addProj(name, homeURL, trackerURL):
		project = get_or_none(Project, name=name)
		if(project):
			return project
		else:
			project = Project.newProject(name, frespo_user, homeURL, trackerURL)
			project.save()
			print('added project '+project.name+':%s'%project.id)
		return project

	addProj('ActiveMQ', 'http://activemq.apache.org/', 'https://issues.apache.org/jira/browse/AMQ')
	addProj('Ant', 'http://ant.apache.org/', 'https://issues.apache.org/bugzilla/buglist.cgi?product=Ant')
	addProj('Ivy', 'http://ant.apache.org/ivy/index.html', 'https://issues.apache.org/jira/browse/IVY')
	addProj('ApacheAXIS', 'http://axis.apache.org/axis/', 'https://issues.apache.org/jira/browse/AXIS')
	addProj('Buildr', 'http://buildr.apache.org/', 'https://issues.apache.org/jira/browse/BUILDR')
	addProj('Cassandra', 'http://cassandra.apache.org/', 'https://issues.apache.org/jira/browse/CASSANDRA')
	addProj('Cayenne', 'http://cayenne.apache.org/', 'https://issues.apache.org/jira/browse/CAY')
	addProj('cglib', 'http://cglib.sourceforge.net/', 'http://sourceforge.net/tracker/?group_id=56933&atid=482368')
	addProj('Classghost', 'http://classghost.sourceforge.net/', 'http://sourceforge.net/tracker/?atid=786235&group_id=153048&func=browse')
	addProj('ClickFramework', 'http://click.apache.org/', 'https://issues.apache.org/jira/browse/CLK')
	addProj('Cocoon', 'http://cocoon.apache.org/3.0/', 'https://issues.apache.org/jira/browse/COCOON3')
	addProj('Android', 'http://code.google.com/p/android/', 'http://code.google.com/p/android/issues')
	addProj('django-pagination', 'http://code.google.com/p/django-pagination/', 'http://code.google.com/p/django-pagination/issues')
	addProj('Gerrit', 'http://code.google.com/p/gerrit/', 'http://code.google.com/p/gerrit/issues')
	addProj('GoogleGuice', 'http://code.google.com/p/google-guice/', 'http://code.google.com/p/google-guice/issues')
	addProj('GoogleGuava', 'http://code.google.com/p/guava-libraries/', 'http://code.google.com/p/guava-libraries/issues')
	addProj('Cofeescript', 'http://coffeescript.org/', 'https://github.com/jashkenas/coffee-script/issues')
	addProj('ApacheFileUpload', 'http://commons.apache.org/fileupload/', 'https://issues.apache.org/jira/browse/FILEUPLOAD')
	addProj('CouchDB', 'http://couchdb.apache.org/', 'https://issues.apache.org/jira/browse/COUCHDB')
	addProj('Cucumber', 'http://cukes.info/', 'https://github.com/cucumber/cucumber/issues')
	addProj('Derby', 'http://db.apache.org/derby/', 'https://issues.apache.org/jira/browse/DERBY')
	addProj('Torque', 'http://db.apache.org/torque/', 'https://issues.apache.org/jira/browse/TORQUE')
	addProj('DWR', 'http://directwebremoting.org/', 'http://directwebremoting.org/jira/browse/DWR')
	addProj('django-social-auth', 'http://django-social-auth.readthedocs.org/', 'https://github.com/omab/django-social-auth/issues')
	addProj('EasyMock', 'http://easymock.org/', 'http://jira.codehaus.org/browse/EASYMOCK')
	addProj('Esfinge', 'http://esfinge.sourceforge.net/', 'http://www.gsw.com.br/esfinge/wp/?page_id=27')
	addProj('Freemarker', 'http://freemarker.sourceforge.net/', 'http://sourceforge.net/tracker/?group_id=794&atid=100794')
	addProj('Git', 'http://git-scm.com/', 'http://git-scm.com/community')
	addProj('Hadoop', 'http://hadoop.apache.org/common/', 'https://issues.apache.org/jira/browse/HADOOP')
	addProj('ApacheHTTPServer', 'http://httpd.apache.org/', 'https://issues.apache.org/bugzilla/buglist.cgi?product=Apache+httpd-2')
	addProj('Flex', 'http://incubator.apache.org/flex/', 'https://issues.apache.org/jira/browse/FLEX')
	addProj('psycopg', 'http://initd.org/psycopg/', 'http://psycopg.lighthouseapp.com/projects/62710/tickets')
	addProj('Jackrabbit', 'http://jackrabbit.apache.org/', 'https://issues.apache.org/jira/browse/JCR')
	addProj('Cactus', 'http://jakarta.apache.org/cactus/', 'https://issues.apache.org/jira/browse/CACTUS')
	addProj('JBehave', 'http://jbehave.org/', 'http://jira.codehaus.org/browse/JBEHAVE')
	addProj('Arquillian', 'http://jboss.org/arquillian', 'https://issues.jboss.org/browse/ARQ')
	addProj('Drools', 'http://jboss.org/drools', 'https://issues.jboss.org/browse/JBRULES')
	addProj('JBossForge', 'http://jboss.org/forge', 'https://issues.jboss.org/browse/FORGE')
	addProj('jBPM', 'http://jboss.org/jbpm', 'https://issues.jboss.org/browse/JBPM')
	addProj('JSFUnit', 'http://jboss.org/jsfunit', 'https://issues.jboss.org/browse/JSFUNIT')
	addProj('RESTEasy', 'http://jboss.org/resteasy', 'https://issues.jboss.org/browse/RESTEASY')
	addProj('RichFaces', 'http://jboss.org/richfaces', 'https://issues.jboss.org/browse/RF')
	addProj('TattleTale', 'http://jboss.org/tattletale', 'https://issues.jboss.org/browse/TTALE')
	addProj('JBossTools', 'http://jboss.org/tools', 'https://issues.jboss.org/browse/JBIDE')
	addProj('Jenkins', 'http://jenkins-ci.org/', 'https://issues.jenkins-ci.org')
	addProj('Jettison', 'http://jettison.codehaus.org/', 'http://jira.codehaus.org/browse/JETTISON')
	addProj('Jetty', 'http://jetty.codehaus.org/', 'http://jira.codehaus.org/browse/JETTY')
	addProj('JMeter', 'http://jmeter.apache.org/', 'https://issues.apache.org/bugzilla/buglist.cgi?product=JMeter')
	addProj('jquery', 'http://jquery.com/', 'http://bugs.jquery.com/')
	addProj('JRuby', 'http://jruby.org/', 'http://jira.codehaus.org/browse/JRUBY')
	addProj('JSTestRunner', 'http://js-testrunner.codehaus.org/', 'http://jira.codehaus.org/browse/JSTR')
	addProj('JUnit', 'http://junit.org/', 'https://github.com/KentBeck/junit/issues')
	addProj('Log4j', 'http://logging.apache.org/log4j/2.0/index.html', 'https://issues.apache.org/jira/browse/LOG4J2')
	addProj('Lucene', 'http://lucene.apache.org/java/', 'https://issues.apache.org/jira/browse/LUCENE')
	addProj('Maven', 'http://maven.apache.org/', 'http://jira.codehaus.org/browse/MNG')
	addProj('MyFaces', 'http://myfaces.apache.org/', 'https://issues.apache.org/jira/browse/MYFACES')
	addProj('Plexus', 'http://plexus.codehaus.org/', 'http://jira.codehaus.org/browse/PLX')
	addProj('Puppet', 'http://puppetlabs.com/', 'http://projects.puppetlabs.com/')
	addProj('coverage.py', 'http://pypi.python.org/pypi/coverage', 'https://bitbucket.org/ned/coveragepy/issues')
	addProj('Rails', 'http://rubyonrails.org/', 'https://github.com/rails/rails/issues')
	addProj('JBossSeam', 'http://seamframework.org/Seam3', 'https://issues.jboss.org/browse/SEAM')
	addProj('Sonar', 'http://sonar.codehaus.org/', 'http://jira.codehaus.org/browse/SONAR')
	addProj('South', 'http://south.aeracode.org/', 'http://south.aeracode.org/')
	addProj('Struts2', 'http://struts.apache.org/2.0', 'https://issues.apache.org/jira/browse/WW')
	addProj('TestNG', 'http://testng.org/', 'https://github.com/cbeust/testng/issues')
	addProj('ApacheTiles', 'http://tiles.apache.org/', 'https://issues.apache.org/jira/browse/TILES')
	addProj('Turbine', 'http://turbine.apache.org/', 'https://issues.apache.org/jira/browse/TRB')
	addProj('TwitterBootstrap', 'http://twitter.github.com/bootstrap', 'https://github.com/twitter/bootstrap/issues')
	addProj('Velocity', 'http://velocity.apache.org/', 'https://issues.apache.org/jira/browse/VELOCITY')
	addProj('Alfresco', 'http://www.alfresco.com/', 'https://issues.alfresco.com/jira/browse/ALF')
	addProj('Antlr', 'http://www.antlr.org/', 'https://github.com/antlr/antlr/issues')
	addProj('Blender', 'http://www.blender.org/', 'http://projects.blender.org/tracker/?atid=498&group_id=9&func=browse')
	addProj('Castor', 'http://www.castor.org/', 'http://jira.codehaus.org/browse/CASTOR')
	addProj('CherryPy', 'http://www.cherrypy.org/', 'https://bitbucket.org/cherrypy/cherrypy/issues')
	addProj('Debian', 'http://www.debian.org', 'http://www.debian.org/Bugs/')
	addProj('Debian', 'http://www.debian.org/', 'http://bugs.debian.org/')
	addProj('AspectJ', 'http://www.eclipse.org/aspectj/', 'https://bugs.eclipse.org/bugs/buglist.cgi?product=AspectJ')
	addProj('FlightGear', 'http://www.flightgear.org/', 'http://code.google.com/p/flightgear-bugs/issues')
	addProj('Gnome', 'http://www.gnome.org/', 'https://bugzilla.gnome.org')
	addProj('Bugzilla', 'http://www.bugzilla.org/', 'https://bugzilla.mozilla.org/buglist.cgi?product=Bugzilla')
	addProj('Gradle', 'http://www.gradle.org/', 'http://issues.gradle.org/browse/GRADLE')
	addProj('ExtGWT', 'http://www.gwt-ext.com/demo/', 'http://www.sencha.com/forum/')
	addProj('Hibernate', 'http://www.hibernate.org/', 'https://hibernate.onjira.com/browse/HHH')
	addProj('javassist', 'http://www.javassist.org/', 'https://issues.jboss.org/browse/JASSIST')
	addProj('JMock', 'http://www.jmock.org/', 'http://jira.codehaus.org/browse/JMOCK')
	addProj('LinuxKernel', 'http://www.kernel.org/', 'https://bugzilla.kernel.org')
	addProj('OpenEHR', 'http://www.openehr.org/', 'http://www.openehr.org/issues')
	addProj('OSQA', 'http://www.osqa.net/', 'http://jira.osqa.net/')
	addProj('Perl', 'http://www.perl.org', 'https://rt.perl.org/perlbug/')
	addProj('PrimeFaces', 'http://www.primefaces.org/', 'http://code.google.com/p/primefaces/issues')
	addProj('prototype', 'http://www.prototypejs.org/', 'https://prototype.lighthouseapp.com/projects/42103')
	addProj('Python', 'http://www.python.org', 'http://bugs.python.org/')
	addProj('Redmine', 'http://www.redmine.org', 'http://www.redmine.org/issues')
	addProj('Ruby', 'http://www.ruby-lang.org/en/', 'http://bugs.ruby-lang.org/')
	addProj('ExtJS', 'http://www.sencha.com/products/extjs/', 'http://www.sencha.com/forum/')
	addProj('SpringFramework', 'http://www.springsource.org/', 'https://jira.springsource.org/browse/SPR')
	addProj('Ubuntu', 'http://www.ubuntu.com/', 'https://bugs.launchpad.net/ubuntu')
	addProj('FOP', 'http://xmlgraphics.apache.org/fop/', 'https://issues.apache.org/bugzilla/buglist.cgi?product=Fop')
	addProj('zenwarch', 'https://bitbucket.org/renzon/zenwarch', 'https://bitbucket.org/renzon/zenwarch/issues')
	addProj('python-paypalx', 'https://github.com/e-loue/python-paypalx', 'https://github.com/e-loue/python-paypalx/issues')
	addProj('django-mailer', 'https://github.com/jtauber/django-mailer/', 'https://github.com/jtauber/django-mailer/issues')
	addProj('Django', 'https://www.djangoproject.com/', 'https://code.djangoproject.com/query')

class Command(NoArgsCommand):

	help = "Popula dados estaticos iniciais"

	option_list = NoArgsCommand.option_list + (
		make_option('--verbose', action='store_true'),
	)
	
	def handle_noargs(self, **options):
		add_initial_projects()





