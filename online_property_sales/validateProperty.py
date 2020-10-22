from forms import PropertyForm
from datetime import datetime

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
        print("here1")
        return False

    if not check_bathrooms(p_n_baths):
        print("here2")
        return False

    if not check_parking(p_n_park):
        print("here3")
        return False

    if not check_parking_features(p_p_features):
        print("here4")
        return False

    if not check_building_size(p_b_size):
        print("here5")
        return False

    if not check_land_size(p_l_size, p_b_size):
        print("here6")
        return False

    if not check_description(p_desc):
        print("here7")
        return False

    if not check_year(p_year):
        print("here8")
        return False

    if not check_inspection_date(p_i_date):
        print("here9")
        return False

    return True

def check_property_type(data):
    if data == None:
        return False
    else:
        return True

def check_address(p_add_unit, p_add_num, p_add_name, p_add_suburb, p_add_state, p_add_pc):
    if len(p_add_unit) > 5:
        return False
    
    if len(p_add_num) > 8:
        return False

    if len(p_add_name) > 50:
        return False

    if len(p_add_suburb) > 50:
        return False

    if p_add_suburb.isdigit():
        return False
    
    if p_add_state == None:
        return False

    if not len(p_add_pc) == 4:
        return False

    if not p_add_pc.isdigit():
        return False
    return True

def check_bedrooms(p_n_beds):
    if not p_n_beds.isdigit():
        return False
    return True

def check_bathrooms(p_n_baths):
    if not p_n_baths.isdigit():
        return False
    return True

def check_parking(p_n_park):
    if not p_n_park.isdigit():
        return False
    return True

def check_parking_features(p_p_features):
    if len(p_p_features) > 1000:
        return False
    return True

def check_building_size(p_b_size):
    if not p_b_size.isdigit():
        return False
    return True

def check_land_size(p_l_size, p_b_size):
    if not check_building_size(p_b_size):
        return False

    if p_b_size > p_l_size:
        return False
    return True

def check_description(p_desc):
    if len(p_desc) > 2500:
        return False
    return True

def check_year(p_year):
    if not len(p_year) == 4:
        return False
    if not p_year.isdigit():
        return False
    return True

def check_inspection_date(p_i_date):
    if datetime.today().date() > p_i_date:
        return False
    return True

def check_edited_updates(form):
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

    if p_add_num or p_add_name or p_add_suburb or p_add_state or p_add_pc:
        if not check_address(p_add_unit, p_add_num, p_add_name, p_add_suburb, p_add_state, p_add_pc):
            return False

    if p_n_beds:
        if not check_bedrooms(p_n_beds):
            return False

    if p_n_baths:
        if not check_bathrooms(p_n_baths):
            return False

    if p_n_park:
        if not check_parking(p_n_park):
            return False

    if p_p_features:
        if not check_parking_features(p_p_features):
            return False
    
    if p_b_size:
        if not check_building_size(p_b_size):
            return False

    if p_l_size:
        if not check_land_size(p_l_size, p_b_size):
            return False

    if p_desc:
        if not check_description(p_desc):
            return False

    if p_year:
        if not check_year(p_year):
            return False

    if p_i_date:
        if not check_inspection_date(p_i_date):
            return False

    return True

