from flask import Flask, jsonify, render_template
from tiny_elephant.in_memory_cluster import InMemoryCluster

app = Flask(__name__)

imc = InMemoryCluster(
    minhash_host='localhost:6379',
    seed=1
)


@app.route('/collapse')
def index():
    return render_template('collapse.html')


@app.route('/codeflower')
def code_flower():
    return render_template('codeflower.html')


@app.route('/keys/<string:key_id>/commons')
def common_keys(key_id):
    if type(key_id) == 'bytes':
        key_id = str(key_id, 'utf-8')
    one_depth_keys = imc.most_common(key_id, count=10)
    res = {
        "name": key_id,
        "children": []
    }
    for one_depth_key in one_depth_keys:
        one_depth_child = {
            "name": one_depth_key[0],
            "size": one_depth_key[1] * 100,
            "children": []
        }
        two_depth_keys = imc.most_common(str(one_depth_key[0], 'utf-8'), 10)
        for two_depth_key in two_depth_keys:
            one_depth_child["children"].append({
                "name": two_depth_key[0],
                "size": two_depth_key[1] * 10
            })
        res['children'].append(one_depth_child)

    return jsonify(res)


if __name__ == '__main__':
    app.run()
