import datetime
from django.test import TestCase
from django.test.client import Client

from profapp.models import Student, SemesterSubject, Exam

MIN_AM_RANGE = 1000
MAX_AM_RANGE = 1100

class TestStudent(TestCase):
    def setUp(self):
        self.c = Client()

	self.math = SemesterSubject(name="Maths", year=2010)
        self.math.save()
        self.math.students.add(*[Student.objects.create(am=i,
                                                        date_enrolled=datetime.datetime.now(),
                                                        semester=1,
                                                        first_name="Chodey",
                                                        last_name="McNumnuts") for i in xrange(MIN_AM_RANGE,MAX_AM_RANGE)])
        self.math.save()

        self.physics = SemesterSubject(name="Physics", year=2013)
        self.physics.save()
        self.physics.students.add(*[Student.objects.get(am=i) for i in xrange(MIN_AM_RANGE,MAX_AM_RANGE)])
        self.physics.save()

	


    def test_list_subj(self):
	r = self.c.get("/profapp/subjects/")
	
	self.assertIn("Physics", r.content)
	self.assertIn("Maths", r.content)

    def test_list_subj_year(self):
        r = self.c.get("/profapp/subjects/Physics/")
        self.assertIn("2013", r.content)
        self.assertNotIn("2010", r.content)
        r = self.c.get("/profapp/subjects/Maths/")
        self.assertIn("2010", r.content)
        self.assertNotIn("2013", r.content)


    def test_subj_stu(self):
	r = self.c.get("/profapp/students/?subj=1")
	for i in xrange(MIN_AM_RANGE,MAX_AM_RANGE):
	    self.assertIn(str(i), r.content)
	
	
