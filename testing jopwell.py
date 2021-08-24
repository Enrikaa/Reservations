class Profile (models.Model):
    """ A candidate's profile information """

    GENDERS = (
        ("Female", "Female"),
        ("Male", "Male"),
        ("Non-Binary/3rd Gender", "Non-Binary/3rd Gender"),
        ("Prefer not to say", "Prefer not to say")
    )

    GENDER_PRONOUNS = (
        ("she, her, hers", "she, her, hers"),
        ("he, him, his", "he, him, his"),
        ("they, them, theirs", "they, them, theirs"),
    )

    AVATAR_COLOR_COMBINATION = [
        ("#28db89", "#02113f"),  # Green/Navy
        ("#f9af38", "#02113f"),  # Orange/Navy
        ("#cbf7e9", "#02113f"),  # Mint/Navy
        ("#28db89", "#cbf7e9"),  # Green/Mint
    ]

    owner = models.OneToOneField(User)

    # About Me
    photo = models.ImageField(upload_to=upload_to_S3, blank=True,
                              verbose_name="Choose Photo")
    location = models.ForeignKey(Location, blank=True, null=True)
    willing_to_relocate = models.BooleanField(default=False,
                                              help_text="Is candidate willing to relocate")
    open_for_remote_work = models.BooleanField(default=False, help_text="Is candidate open for remote work")

    gender = models.CharField(choices=GENDERS, max_length=100, default=None,
                              blank=True, null=True)
    gender_pronouns = models.CharField(choices=GENDER_PRONOUNS, max_length=100, default=None,
                                       blank=True, null=True)

    birthday = models.DateField(blank=True, null=True)
    ethnicities = models.ManyToManyField(Ethnicity, blank=True)
    personal_statement = models.TextField(
        max_length=15000, blank=True, null=True)
    high_school = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(max_length=1000, blank=True, null=True)

    # Resume / Work Experience
    resume = models.FileField(upload_to=upload_to_S3, blank=True,
                              verbose_name="Choose Resume")
    is_resume_active = models.BooleanField(default=False)
    resume_pdf = models.FileField(upload_to=upload_to_S3, blank=True)
    has_parsed_resume = models.BooleanField(default=False)
    show_resume = models.BooleanField(default=True, help_text="should resume be shown to candidate")
    resume_last_updated_at = models.DateTimeField(blank=True, null=True)

    # Candidate Work Preferences
    desired_industries = models.ManyToManyField(Industry, blank=True)
    desired_job_roles = models.ManyToManyField(JobRole, blank=True)
    desired_job_level = models.ForeignKey(
        JobExperienceLevel, blank=True, null=True, on_delete=models.SET_NULL)
    desired_work_environment = models.ManyToManyField(
        WorkEnvironment, blank=True)
    desired_company_size = models.ManyToManyField(CompanySize, blank=True)
    desired_locations = models.ManyToManyField(
        Location, blank=True, related_name="desired_locations")

    # Don't use desired_region in code.  Only maintained for historical analysis of data
    desired_region = models.ManyToManyField(Region, blank=True)

    is_ambassador = models.BooleanField(default=False)
    work_experience_other = models.URLField(
        blank=True, null=True, help_text="Personal Website Link")
    short_candidate = models.BooleanField(default=False)
    is_undergraduate = models.BooleanField(default=False)
    show_tooltips_dashboard = models.BooleanField(default=True)
    show_tooltips_profile = models.BooleanField(default=True)

    years_experience_inferred = models.IntegerField(blank=True, null=True,
                                                    validators=[MinValueValidator(0)])
    leadership_moment = models.TextField(max_length=15000, default='',
                                         blank=True, null=False,
                                         help_text="Tell us about an experience in which you demonstrated "
                                         "leadership. Feel free to draw from an experience "
                                         "outside of the workplace. (200 words max).")

    indexed_at = models.DateTimeField(blank=True, null=True,
                                      help_text="Last time this candidate was indexed for candidate "
                                      "search.")
    last_visit_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date created.")
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Date last modified.")

    objects = CandidateManager()

    # indicates that a candidate is currently within 'Jopwell Select'
    # in this case, there is a record for the candidate in models.candidate_classifications.CandidateRecruiterBucket
    # typically this flag is set in the save method of CandidateRecruiterBucket
    is_active_on_pro = models.BooleanField(default=False, help_text="this flag indicates that the candidate is a member \
                                                                    of 'Jopwell Select'")
    is_hidden_from_search = models.BooleanField(default=False,
                                                help_text="Profile with this flag is hidden form search results.")
    is_jopwell_recruiter_updates_allowed = models.BooleanField(
        default=True, help_text=u"this flag indicates that a Jopwell recruiter is allowed to make updates to candidate's profile")
    is_jopwell_recruiter_updates_allowed_last_updated = models.DateTimeField(blank=True, null=True)
    is_updated_by_jopwell_recruiter_since_last_seen = models.BooleanField(
        default=False, help_text=u"Whether the profile was updated by a Jopwell recruiter and candidate has not seen changes.")
    self_selected_as_open_to_opportunities = models.CharField(max_length=25, choices=SEARCH_ELIGILITY_STATUS_CHOICES,
                                                              default="OTO",
                                                              help_text=u"Whether this candidate indicated to be open to new opportunities.")
    self_reported_professional_career_start_year = models.IntegerField(blank=True, null=True,
                                                                       verbose_name="The self-reported start year of the candidate's professional career",
                                                                       validators=[MinValueValidator(1950)])
    external_platform_surfaced_on = models.CharField(max_length=50, blank=True)

    avatar_foreground = models.CharField(max_length=7, null=True, blank=True)
    avatar_background = models.CharField(max_length=7, null=True, blank=True)

    is_new = models.BooleanField(default=False, help_text=u"Whether a candidate has just signed up.")