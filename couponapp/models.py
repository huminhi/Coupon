# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class CappAccountPageSetting(models.Model):
    id = models.IntegerField(primary_key=True)
    account_type = models.CharField(max_length=135)
    main_title = models.CharField(max_length=300)
    sub_title1 = models.CharField(max_length=300)
    sub_title1_description = models.TextField()
    sub_title2 = models.CharField(max_length=300)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_account_page_setting'

class CappAdminLogin(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=75)
    password = models.CharField(max_length=135)
    admin_type = models.CharField(max_length=75)
    email = models.CharField(max_length=300)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=90)
    birthday = models.CharField(max_length=90)
    country_id = models.IntegerField()
    state_id = models.IntegerField()
    state_name = models.CharField(max_length=240)
    zipcode = models.IntegerField()
    gender = models.CharField(max_length=60)
    admin_image = models.CharField(max_length=300)
    modules_access = models.TextField()
    login_status = models.CharField(max_length=45)
    display_status = models.CharField(max_length=15)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_admin_login'

class CappAppealReason(models.Model):
    id = models.IntegerField(primary_key=True)
    appeal_reason = models.TextField()
    date_time = models.CharField(max_length=300)
    dispaly_status = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_appeal_reason'

class CappBanners(models.Model):
    banner_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=600)
    description = models.TextField()
    link_url = models.TextField()
    banner_image = models.CharField(max_length=765)
    display_status = models.CharField(max_length=135)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_banners'

class CappBusinessContactUs(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    subject = models.TextField()
    message = models.TextField()
    upload_file_name = models.CharField(max_length=300)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    class Meta:
        db_table = u'capp_business_contact_us'

class CappCashbackRewards(models.Model):
    cashback_id = models.IntegerField(primary_key=True)
    cashback_rewards = models.FloatField()
    cash_to_points_rewards_cash = models.FloatField()
    cash_to_points_rewards_points = models.FloatField()
    points_to_cash_rewards_cash = models.FloatField()
    points_to_cash_rewards_points = models.FloatField()
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_cashback_rewards'

class CappCategories(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=765)
    category_image = models.CharField(max_length=300)
    access_level = models.CharField(max_length=300)
    language = models.CharField(max_length=450)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_categories'

class CappCities(models.Model):
    city_id = models.IntegerField(primary_key=True)
    country_id = models.IntegerField()
    city_name = models.CharField(max_length=300)
    district_name = models.CharField(max_length=300)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_cities'

class CappCmsPages(models.Model):
    page_id = models.IntegerField(primary_key=True)
    main_page_id = models.IntegerField()
    page_name = models.CharField(max_length=150)
    page_url = models.CharField(max_length=300)
    page_title = models.CharField(max_length=150)
    meta_keyword = models.CharField(max_length=450)
    meta_description = models.CharField(max_length=750)
    page_content = models.TextField()
    image_name = models.ImageField(max_length=765)
    display_status = models.CharField(max_length=135)
    status = models.CharField(max_length=135)
    class Meta:
        db_table = u'capp_cms_pages'

class CappCommissions(models.Model):
    commission_id = models.IntegerField(primary_key=True)
    status_name = models.CharField(max_length=300)
    commission_type = models.CharField(max_length=75)
    fixed_amount = models.FloatField()
    percentage_amount = models.FloatField()
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_commissions'

class CappConfigureSettings(models.Model):
    setting_id = models.IntegerField(primary_key=True)
    admin_id = models.IntegerField()
    enable_alphabet_search = models.CharField(max_length=75)
    notification_email_addresses = models.TextField()
    expired_coupon_email_subject = models.CharField(max_length=765)
    expired_coupon_email_msg = models.TextField()
    share_coupon_email_subject = models.CharField(max_length=765)
    share_coupon_email_msg = models.TextField()
    store_added_email_subject = models.CharField(max_length=765)
    store_added_email_msg = models.TextField()
    order_acknowledge_email_subject = models.CharField(max_length=765)
    order_acknowledge_email_msg = models.TextField()
    purchase_confirm_email_subject = models.CharField(max_length=765)
    purchase_confirm_email_msg = models.TextField()
    report_coupon_email_subject = models.CharField(max_length=765)
    report_coupon_email_msg = models.TextField()
    embed_code_email_subject = models.CharField(max_length=765)
    embed_code_email_msg = models.TextField()
    store_logo_width = models.IntegerField()
    store_logo_height = models.IntegerField()
    coupon_image_width = models.IntegerField()
    coupon_image_height = models.IntegerField()
    thumbnail_width = models.IntegerField()
    thumbnail_height = models.IntegerField()
    word_limit_for_printable_description = models.IntegerField()
    no_of_codes = models.IntegerField()
    share_your_code = models.CharField(max_length=300)
    remember_your_code = models.CharField(max_length=300)
    code_limit = models.CharField(max_length=135)
    code_valid_for_user_id = models.CharField(max_length=765)
    code_length = models.IntegerField()
    code_include = models.CharField(max_length=135)
    code_expiration = models.IntegerField()
    default_list_length = models.IntegerField()
    display_similar_coupon = models.CharField(max_length=75)
    display_similar_coupons_by = models.CharField(max_length=75)
    show_thumbnails = models.CharField(max_length=75)
    show_review = models.CharField(max_length=75)
    show_report_btn = models.CharField(max_length=75)
    show_printer_btn = models.CharField(max_length=75)
    show_fb_like = models.CharField(max_length=75)
    show_tweet_btn = models.CharField(max_length=75)
    show_send_btn = models.CharField(max_length=75)
    show_prints = models.CharField(max_length=75)
    show_timer_on_list = models.CharField(max_length=75)
    show_timer_on_details = models.CharField(max_length=75)
    show_author = models.CharField(max_length=75)
    show_store = models.CharField(max_length=75)
    enable_fb_comment = models.CharField(max_length=75)
    fb_comment_box_width = models.IntegerField()
    coupon_types = models.CharField(max_length=75)
    display_status = models.CharField(max_length=75)
    class Meta:
        db_table = u'capp_configure_settings'

class CappContact(models.Model):
    id = models.IntegerField(primary_key=True)
    discuss_about = models.TextField()
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=450)
    company = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=135)
    hear_about = models.CharField(max_length=450)
    description = models.TextField()
    upload_file_name = models.CharField(max_length=750)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=135)
    status = models.CharField(max_length=135)
    class Meta:
        db_table = u'capp_contact'

class CappCountries(models.Model):
    country_id = models.IntegerField(primary_key=True)
    country_name = models.CharField(max_length=300)
    country_code_2 = models.CharField(max_length=6)
    country_code_3 = models.CharField(max_length=9)
    display_status = models.CharField(max_length=135)
    status = models.CharField(max_length=135)
    class Meta:
        db_table = u'capp_countries'

class CappCouponCodes(models.Model):
    coupon_code_id = models.IntegerField(primary_key=True)
    coupon_id = models.IntegerField()
    coupon_code = models.CharField(max_length=135)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=75)
    class Meta:
        db_table = u'capp_coupon_codes'

class CappCouponLikes(models.Model):
    id = models.IntegerField(primary_key=True)
    store_id = models.IntegerField()
    coupon_id = models.IntegerField()
    user_id = models.IntegerField()
    like_status = models.CharField(max_length=15)
    dislike_feedback = models.TextField()
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_coupon_likes'

class CappCouponRating(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    coupon_id = models.IntegerField()
    rating = models.CharField(max_length=300)
    date_time = models.CharField(max_length=450)
    display_status = models.CharField(max_length=135)
    class Meta:
        db_table = u'capp_coupon_rating'

class CappCouponReviews(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    store_id = models.IntegerField()
    coupon_id = models.IntegerField()
    review_comment = models.TextField()
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_coupon_reviews'

class CappCoupons(models.Model):
    coupon_id = models.IntegerField(primary_key=True)
    coupon_name = models.CharField(max_length=300)
    store_id = models.IntegerField()
    service_plan_id = models.IntegerField()
    customized_amount = models.IntegerField()
    customized_validity = models.CharField(max_length=180)
    admin_commission = models.IntegerField()
    pos = models.CharField(max_length=75)
    tracking = models.CharField(max_length=75)
    category_id = models.IntegerField()
    country_id = models.IntegerField()
    city_id = models.IntegerField()
    district_name = models.CharField(max_length=600)
    image_name = models.CharField(max_length=300)
    description = models.TextField()
    start_time = models.CharField(max_length=300)
    end_time = models.CharField(max_length=300)
    expiration_hour = models.IntegerField()
    discount_type = models.CharField(max_length=75)
    code_limit = models.CharField(max_length=75)
    percentage_amount = models.FloatField()
    fixed_amount = models.FloatField()
    discount_description = models.TextField()
    hotseller = models.CharField(max_length=75)
    access_level = models.CharField(max_length=135)
    valid_at = models.CharField(max_length=600)
    keywords = models.CharField(max_length=600)
    total_codes = models.IntegerField()
    language = models.CharField(max_length=135)
    meta_keywords = models.CharField(max_length=600)
    meta_description = models.TextField()
    author = models.CharField(max_length=300)
    robots = models.CharField(max_length=300)
    facebook_like_button = models.CharField(max_length=75)
    tweet_button = models.CharField(max_length=75)
    send_button = models.CharField(max_length=75)
    display_store = models.CharField(max_length=75)
    display_status = models.CharField(max_length=75)
    date_time = models.CharField(max_length=300)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_coupons'

class CappFaqManagement(models.Model):
    id = models.IntegerField(primary_key=True)
    faq_questions = models.TextField()
    faq_answers = models.TextField()
    faq_type = models.CharField(max_length=300)
    display_status = models.CharField(max_length=300)
    date_time = models.CharField(max_length=300)
    status = models.CharField(max_length=765)
    class Meta:
        db_table = u'capp_faq_management'

class CappMonths(models.Model):
    month_id = models.IntegerField(primary_key=True)
    month_index = models.CharField(max_length=6)
    month_name = models.CharField(max_length=165)
    display_status = models.CharField(max_length=75)
    class Meta:
        db_table = u'capp_months'

class CappNewsletter(models.Model):
    newsletter_id = models.IntegerField(primary_key=True)
    category_id = models.IntegerField()
    subject = models.CharField(max_length=300)
    newsletter = models.TextField()
    class Meta:
        db_table = u'capp_newsletter'

class CappNewsletterSubscribers(models.Model):
    newsletter_id = models.IntegerField(primary_key=True)
    email_id = models.CharField(max_length=450)
    category_id = models.IntegerField()
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_newsletter_subscribers'

class CappOrders(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    store_id = models.IntegerField()
    coupon_id = models.IntegerField()
    coupon_code_id = models.CharField(max_length=300)
    service_plan_id = models.IntegerField()
    category_id = models.IntegerField()
    city_id = models.IntegerField()
    reciept_number = models.CharField(max_length=465)
    total_bill = models.FloatField()
    reward_points = models.IntegerField()
    order_status = models.CharField(max_length=135)
    payment_method = models.CharField(max_length=300)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_orders'

class CappPaymentMethods(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=765)
    description = models.TextField()
    display_status = models.CharField(max_length=150)
    date_time = models.CharField(max_length=600)
    status = models.CharField(max_length=150)
    class Meta:
        db_table = u'capp_payment_methods'

class CappPaymentSetting(models.Model):
    id = models.IntegerField(primary_key=True)
    payment_type = models.CharField(max_length=300)
    payment_setting = models.CharField(max_length=135)
    account_number = models.CharField(max_length=300)
    payable_to = models.CharField(max_length=600)
    bank_name = models.CharField(max_length=600)
    bank_branch = models.CharField(max_length=600)
    swift_address_aba_number = models.TextField()
    payment_mailing_address = models.TextField()
    paypal_setting = models.CharField(max_length=135)
    paypal_settings_enabled = models.CharField(max_length=75)
    paypal_email = models.CharField(max_length=600)
    payment_mode = models.CharField(max_length=135)
    currency = models.CharField(max_length=300)
    store_name = models.CharField(max_length=300)
    cash_delivery_full_name = models.CharField(max_length=600)
    cash_delivery_address = models.CharField(max_length=765)
    cash_delivery_phone_no = models.CharField(max_length=135)
    cash_delivery_email = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    date_time = models.CharField(max_length=300)
    class Meta:
        db_table = u'capp_payment_setting'

class CappPrintedCouponCodes(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    coupon_id = models.IntegerField()
    coupon_code_id = models.IntegerField()
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    class Meta:
        db_table = u'capp_printed_coupon_codes'

class CappProducts(models.Model):
    product_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    store_id = models.IntegerField()
    product_name = models.CharField(max_length=300)
    view_count = models.IntegerField()
    view_status = models.CharField(max_length=75)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    class Meta:
        db_table = u'capp_products'

class CappRecentActivity(models.Model):
    recent_activity_id = models.IntegerField(primary_key=True)
    activity_msg = models.TextField()
    type = models.CharField(max_length=300)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_recent_activity'

class CappSearchKeywordsEngine(models.Model):
    keyword_id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=465)
    display_status = models.CharField(max_length=75)
    date_time = models.CharField(max_length=300)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_search_keywords_engine'

class CappServicePlans(models.Model):
    id = models.IntegerField(primary_key=True)
    service_title = models.CharField(max_length=300)
    amount = models.IntegerField()
    validity = models.CharField(max_length=765)
    commission_type = models.CharField(max_length=135)
    admin_commission = models.IntegerField()
    pos = models.CharField(max_length=15)
    tracking = models.CharField(max_length=15)
    description = models.TextField()
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_service_plans'

class CappSocialMedia(models.Model):
    social_media_id = models.IntegerField(primary_key=True)
    facebook_url = models.TextField()
    twitter_url = models.TextField()
    pinterest_url = models.TextField()
    date_time = models.CharField(max_length=300)
    class Meta:
        db_table = u'capp_social_media'

class CappStorePageTemplate(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    image_name = models.CharField(max_length=765)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_store_page_template'

class CappStorePayments(models.Model):
    id = models.IntegerField(primary_key=True)
    store_id = models.IntegerField()
    service_plan_id = models.IntegerField()
    from_date = models.CharField(max_length=450)
    to_date = models.CharField(max_length=450)
    paid = models.FloatField()
    balance = models.FloatField()
    due_date = models.CharField(max_length=450)
    payment_status = models.CharField(max_length=135)
    late_fee = models.FloatField()
    date_time = models.CharField(max_length=450)
    display_status = models.CharField(max_length=135)
    class Meta:
        db_table = u'capp_store_payments'

class CappStores(models.Model):
    store_id = models.IntegerField(primary_key=True)
    admin_id = models.IntegerField()
    city_id = models.IntegerField()
    service_plan_id = models.IntegerField()
    store_name = models.CharField(max_length=465)
    website_url = models.TextField()
    description = models.TextField()
    street_address = models.CharField(max_length=765)
    phone_number = models.CharField(max_length=150)
    logo = models.CharField(max_length=300)
    language = models.CharField(max_length=300)
    show_street_address = models.CharField(max_length=75)
    access_level = models.CharField(max_length=300)
    show_logo = models.CharField(max_length=75)
    show_url = models.CharField(max_length=75)
    store_status = models.CharField(max_length=150)
    uptodate_revenue = models.CharField(max_length=600)
    uptodate_balance = models.CharField(max_length=600)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_stores'

class CappTestimonials(models.Model):
    testimonial_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    testimonials = models.TextField()
    active_status = models.CharField(max_length=30)
    date_time = models.CharField(max_length=450)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_testimonials'

class CappUserGetCash(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    payment_method = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=150)
    paypal_email = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_user_get_cash'

class CappUsers(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_type = models.CharField(max_length=150)
    store_owner_id = models.CharField(max_length=300)
    store_id = models.IntegerField()
    admin_id = models.IntegerField()
    staff_store_id = models.IntegerField()
    service_plan_id = models.IntegerField()
    username = models.CharField(max_length=300)
    name = models.CharField(max_length=600)
    email = models.CharField(max_length=765)
    password = models.CharField(max_length=135)
    cashier_password = models.CharField(max_length=300)
    street_address = models.CharField(max_length=600)
    city = models.IntegerField()
    district = models.CharField(max_length=300)
    phone_no = models.CharField(max_length=60)
    category_id = models.CharField(max_length=600)
    gender = models.CharField(max_length=75)
    user_image = models.CharField(max_length=450)
    point_reward = models.FloatField()
    facebook_id = models.CharField(max_length=300)
    send_me_offers = models.CharField(max_length=75)
    verified_status = models.CharField(max_length=75)
    fees_paid = models.CharField(max_length=150)
    last_visit = models.CharField(max_length=300)
    date_time = models.CharField(max_length=600)
    login_status = models.CharField(max_length=135)
    display_status = models.CharField(max_length=75)
    status = models.CharField(max_length=6)
    class Meta:
        db_table = u'capp_users'

class CappVideoClips(models.Model):
    video_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=135)
    video_title = models.CharField(max_length=300)
    video_description = models.TextField()
    video_file_name = models.CharField(max_length=450)
    date_time = models.CharField(max_length=450)
    display_status = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    class Meta:
        db_table = u'capp_video_clips'

class CappWishlist(models.Model):
    wishlist_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    store_id = models.IntegerField()
    product_id = models.IntegerField()
    wishlist_count = models.IntegerField()
    date_time = models.CharField(max_length=300)
    display_status = models.CharField(max_length=75)
    class Meta:
        db_table = u'capp_wishlist'

class WpCommentmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    comment_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = u'wp_commentmeta'

class WpComments(models.Model):
    comment_id = models.BigIntegerField(primary_key=True, db_column='comment_ID') # Field name made lowercase.
    comment_post_id = models.BigIntegerField(db_column='comment_post_ID') # Field name made lowercase.
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=300)
    comment_author_url = models.CharField(max_length=600)
    comment_author_ip = models.CharField(max_length=300, db_column='comment_author_IP') # Field name made lowercase.
    comment_date = models.DateTimeField()
    comment_date_gmt = models.DateTimeField()
    comment_content = models.TextField()
    comment_karma = models.IntegerField()
    comment_approved = models.CharField(max_length=60)
    comment_agent = models.CharField(max_length=765)
    comment_type = models.CharField(max_length=60)
    comment_parent = models.BigIntegerField()
    user_id = models.BigIntegerField()
    class Meta:
        db_table = u'wp_comments'

class WpLinks(models.Model):
    link_id = models.BigIntegerField(primary_key=True)
    link_url = models.CharField(max_length=765)
    link_name = models.CharField(max_length=765)
    link_image = models.CharField(max_length=765)
    link_target = models.CharField(max_length=75)
    link_description = models.CharField(max_length=765)
    link_visible = models.CharField(max_length=60)
    link_owner = models.BigIntegerField()
    link_rating = models.IntegerField()
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=765)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=765)
    class Meta:
        db_table = u'wp_links'

class WpOptions(models.Model):
    option_id = models.BigIntegerField(primary_key=True)
    option_name = models.CharField(unique=True, max_length=255)
    option_value = models.TextField()
    autoload = models.CharField(max_length=60)
    class Meta:
        db_table = u'wp_options'

class WpPostmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    post_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = u'wp_postmeta'

class WpPosts(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID')
    post_author = models.BigIntegerField()
    post_date = models.DateTimeField()
    post_date_gmt = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=60)
    comment_status = models.CharField(max_length=60)
    ping_status = models.CharField(max_length=60)
    post_password = models.CharField(max_length=60)
    post_name = models.CharField(max_length=600)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField()
    post_modified_gmt = models.DateTimeField()
    post_content_filtered = models.TextField()
    post_parent = models.BigIntegerField()
    guid = models.CharField(max_length=765)
    menu_order = models.IntegerField()
    post_type = models.CharField(max_length=60)
    post_mime_type = models.CharField(max_length=300)
    comment_count = models.BigIntegerField()
    class Meta:
        db_table = u'wp_posts'

class WpTermRelationships(models.Model):
    object_id = models.BigIntegerField(primary_key=True)
    term_taxonomy_id = models.BigIntegerField()
    term_order = models.IntegerField()
    class Meta:
        db_table = u'wp_term_relationships'

class WpTermTaxonomy(models.Model):
    term_taxonomy_id = models.BigIntegerField(primary_key=True)
    term_id = models.BigIntegerField(unique=True)
    taxonomy = models.CharField(max_length=96)
    description = models.TextField()
    parent = models.BigIntegerField()
    count = models.BigIntegerField()
    class Meta:
        db_table = u'wp_term_taxonomy'

class WpTermmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    term_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = u'wp_termmeta'

class WpTerms(models.Model):
    term_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=600)
    slug = models.CharField(max_length=600)
    term_group = models.BigIntegerField()
    class Meta:
        db_table = u'wp_terms'

class WpUsermeta(models.Model):
    umeta_id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = u'wp_usermeta'

class WpUsers(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    user_login = models.CharField(max_length=180)
    user_pass = models.CharField(max_length=765)
    user_nicename = models.CharField(max_length=150)
    user_email = models.CharField(max_length=300)
    user_url = models.CharField(max_length=300)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=765)
    user_status = models.IntegerField()
    display_name = models.CharField(max_length=750)
    class Meta:
        db_table = u'wp_users'

