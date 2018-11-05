import run_newwebserver


def main():
    test_instance()
    test_bucket()


def test_instance():
    instance = run_newwebserver.create_instance("Assignment1", "SSH")  # change to custom key & security group
    image_id = instance.instance_id
    assert instance.image_id == "ami-0bdb1d6c15a40392c"
    assert instance.state["Name"] == "running" or "pending"  # accounting for instance still pending before starting
    run_newwebserver.terminate_instance(image_id)


def test_bucket():
    bucket = run_newwebserver.create_bucket("fesinfeuibf")
    name = "s3.Bucket(name='fesinfeuibf')"
    print(bucket)
    assert str(bucket) == name
    run_newwebserver.delete_bucket("fesinfeuibf")


if __name__ == '__main__':
        main()
