from forms import PropertyForm
from datetime import datetime
from flask import flash

def check_all_details(form):
    p_type = form.property_type.data
    p_add_unit = form.add_unit.data
    p_add_num = form.add_num.data
    p_add_name = form.add_name.data
    p_add_suburb = form.add_suburb.data
    p_add_state = form.add_state.data
    p_add_pc = form.add_pc.data
    p_n_beds = form.num_bedrooms.data
    p_n_baths = form.num_bathrooms.data
    p_n_park = form.num_parking.data
    p_p_features = form.parking_features.data
    p_b_size = form.building_size.data
    p_l_size = form.land_size.data
    p_desc = form.description.data
    p_year = form.year_built.data
    p_i_date = form.inspection_date.data

    if not check_property_type(p_type):
        return False

    if not check_address(p_add_unit, p_add_num, p_add_name, p_add_suburb, p_add_state, p_add_pc):
        return False

    if not check_bedrooms(p_n_beds):
        return False

    if not check_bathrooms(p_n_baths):
        return False

    if not check_parking(p_n_park):
        return False

    if not check_parking_features(p_p_features):
        return False

    if not check_building_size(p_b_size):
        
        return False

    if not check_land_size(p_l_size, p_b_size):
        return False

    if not check_description(p_desc):
        return False

    if not check_year(p_year):
        return False

    if not check_inspection_date(p_i_date):
        return False

    return True

def check_property_type(data):
    if data == None:
        return False
    else:
        return True

def check_address(p_add_unit, p_add_num, p_add_name, p_add_suburb, p_add_state, p_add_pc):
    if len(p_add_unit) > 5:
        flash('Length of unit number is limited to 5 digits','danger')
        return False
    
    if len(p_add_num) > 8:
        flash('Length of street number is limited to 8 digits','danger')
        return False

    if len(p_add_name) > 50:
        flash('Length of street name is limited to 50 characters','danger')
        return False

    if len(p_add_suburb) > 50:
        flash('Length of suburb is limited to 50 characters','danger')
        return False

    if not p_add_unit.isdigit():
        flash('Only accept digits for unit name','danger')
        return False

    if not p_add_num.isdigit():
        flash('Only accept digits for street number','danger')
        return False

    if  p_add_name.isdigit():
        flash('Only accept string for street name','danger')
        return False

    if p_add_suburb.isdigit():
        flash('Only accept string for suburb','danger')
        return False
    
    if p_add_state == None:
        flash('Please select state','danger')
        return False

    if not len(p_add_pc) == 4:
        flash('Please enter exact 4 digits for postcode','danger')
        return False

    if not p_add_pc.isdigit():
        flash('Please enter exact 4 digits for postcode','danger')
        return False
    return True

def check_bedrooms(p_n_beds):
    if not p_n_beds.isdigit():
        flash('Only numbers for number of bedroom','danger')
        return False
    return True

def check_bathrooms(p_n_baths):
    if not p_n_baths.isdigit():
        flash('Only numbers for number of bathroom','danger')
        return False
    return True

def check_parking(p_n_park):
    if not p_n_park.isdigit():
        flash('Only numbers for number of parking spots','danger')
        return False
    return True

def check_parking_features(p_p_features):
    if len(p_p_features) > 1000:
        flash('Parking features should be limited in 1000 characters','danger')
        return False
    return True

def check_building_size(p_b_size):
    if not p_b_size.isdigit():
        flash('Building size is digital only','danger')
        return False
    return True

def check_land_size(p_l_size, p_b_size):
    if not check_building_size(p_b_size):
        flash('Land size is digital only and should be greater than building size','danger')
        return False

    if p_b_size > p_l_size:
        flash('Land size should be greater or equal to building size','danger')
        return False
    return True

def check_description(p_desc):
    if len(p_desc) > 2500:
        flash('Description should be limited in 2500 characters','danger')
        return False
    return True

def check_year(p_year):
    if not len(p_year) == 4:
        flash('Year of Built should be in form: YYYY and eariler than this year','danger')
        return False
    if not p_year.isdigit():
        flash('Year of Built should be in form: YYYY and eariler than this year','danger')
        return False
    if int(p_year) > 2020:
        flash('Year of Built should be in form: YYYY and eariler than this year','danger')
        return False
    return True

def check_inspection_date(p_i_date):
    if datetime.today().date() > p_i_date:
        flash('Inspection date in form: YYYY-MM-DD, and should later than today','danger')
        return False
    return True

# def check_edited_updates(form):
#     p_type = form.property_type.data
#     p_add_unit = form.add_unit.data
#     p_add_num = form.add_num.data
#     p_add_name = form.add_name.data
#     p_add_suburb = form.add_suburb.data
#     p_add_state = form.add_state.data
#     p_add_pc = form.add_pc.data
#     p_n_beds = form.num_bedrooms.data
#     p_n_baths = form.num_bathrooms.data
#     p_n_park = form.num_parking.data
#     p_p_features = form.parking_features.data
#     p_b_size = form.building_size.data
#     p_l_size = form.land_size.data
#     p_desc = form.description.data
#     p_year = form.year_built.data
#     p_i_date = form.inspection_date.data

#     if not check_property_type(p_type):
#         return False

#     if p_add_num or p_add_name or p_add_suburb or p_add_state or p_add_pc:
#         if not check_address(p_add_unit, p_add_num, p_add_name, p_add_suburb, p_add_state, p_add_pc):
#             return False

#     if p_n_beds:
#         if not check_bedrooms(p_n_beds):
#             return False

#     if p_n_baths:
#         if not check_bathrooms(p_n_baths):
#             return False

#     if p_n_park:
#         if not check_parking(p_n_park):
#             return False

#     if p_p_features:
#         if not check_parking_features(p_p_features):
#             return False
    
#     if p_b_size:
#         if not check_building_size(p_b_size):
#             return False

#     if p_l_size:
#         if not check_land_size(p_l_size, p_b_size):
#             return False

#     if p_desc:
#         if not check_description(p_desc):
#             return False

#     if p_year:
#         if not check_year(p_year):
#             return False

#     if p_i_date:
#         if not check_inspection_date(p_i_date):
#             return False

#     return True

