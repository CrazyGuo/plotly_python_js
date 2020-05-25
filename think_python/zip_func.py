car_state = [       ('draft', '至局长'), 
                    ('department_confirm', '至领导'),
                    ('discipline_confirm', '至纪委'),
                    ('confirm', '已完成'), 
                    ('refused', '已退回')
            ]  
roles = [   ('department_manager', '局长角色'), 
            ('super_manager','领导角色'), 
            ('discipline', '纪委角色')
        ]

def get_approve_matrix():
    result = []
    current_state =  car_state[0:3]
    next_state =  car_state[1:4]
    for current, next_st, role in zip(current_state, next_state, roles):
        mitem = {   'flow_state': current[0],
                    'next_state': next_st[0],
                    'approve_role': role[0]
         }
        result.append((0,0,mitem))
    return result

res = get_approve_matrix()
print(res)