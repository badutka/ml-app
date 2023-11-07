from mlengine.pipelines.pipeline import run_pipeline


def main():
    run_pipeline(option='data_ingestion')
    run_pipeline(option='data_validation_pre_t')
    run_pipeline(option='data_transformation')
    run_pipeline(option='data_validation_post_t')
    run_pipeline(option='data_split')


if __name__ == "__main__":
    main()
