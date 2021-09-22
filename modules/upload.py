from HCPInterface.hcp import HCPManager


def hcp_upload(json_file, sample_seqs, dt_str, endpoint, aws_key_id, aws_secret_key, bucket):

    try:
        hcpm = HCPManager(endpoint, aws_key_id, aws_secret_key)
        hcpm.attach_bucket(bucket)

        hcpm.upload_file(str(json_file), dt_str, metadata={'dt_tag': dt_str, 'type': 'json'}, silent=True)

        for sample in sample_seqs:
            for file in sample_seqs[sample]:
                hcpm.upload_file(str(file), dt_str,
                                 metadata={'dt_tag': dt_str, 'type': 'fastq', 'sample': sample}, silent=True)

        return True

    except:
        return False

