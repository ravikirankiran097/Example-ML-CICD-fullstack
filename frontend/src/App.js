import React, {Component,} from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            result: "Click predict to find out!",
            formData: {
                capShape: '',
                capSurface: '',
                capColour: '',
                bruises: '',
                odour: '',
                gillAttachment: '',
                gillSpacing: '',
                gillSize: '',
                gillColour: '',
                stalkShape: '',
                stalkRoot: '',
                stalkSurfaceAboveRing: '',
                stalkSurfaceBelowRing: '',
                stalkColourAboveRing: '',
                stalkColourBelowRing: '',
                veilType: '',
                veilColour: '',
                ringNumber: '',
                ringType: '',
                sporePrintColour: '',
                population: '',
                habitat: ''
            },
            pastPredictions: [
                {
                    id: 1,
                    dateTime: '12 Apr 2020 11.06PM',
                    features: {
                        capShape: '',
                        capSurface: '',
                        capColour: '',
                        bruises: '',
                        odour: '',
                        gillAttachment: '',
                        gillSpacing: '',
                        gillSize: '',
                        gillColour: '',
                        stalkShape: '',
                        stalkRoot: '',
                        stalkSurfaceAboveRing: '',
                        stalkSurfaceBelowRing: '',
                        stalkColourAboveRing: '',
                        stalkColourBelowRing: '',
                        veilType: '',
                        veilColour: '',
                        ringNumber: '',
                        ringType: '',
                        sporePrintColour: '',
                        population: '',
                        habitat: ''
                    }, prediction: 'Poisonous'
                },
                {
                    id: 2,
                    dateTime: '12 Apr 2020 11.06PM',
                    features: {
                        capShape: '',
                        capSurface: '',
                        capColour: '',
                        bruises: '',
                        odour: '',
                        gillAttachment: '',
                        gillSpacing: '',
                        gillSize: '',
                        gillColour: '',
                        stalkShape: '',
                        stalkRoot: '',
                        stalkSurfaceAboveRing: '',
                        stalkSurfaceBelowRing: '',
                        stalkColourAboveRing: '',
                        stalkColourBelowRing: '',
                        veilType: '',
                        veilColour: '',
                        ringNumber: '',
                        ringType: '',
                        sporePrintColour: '',
                        population: '',
                        habitat: ''
                    }, prediction: 'Not Poisonous'
                }
            ]
        }
    }

    handleChange = (event) => {
        const value = event.target.value;
        const name = event.target.name;
        let formData = this.state.formData;
        formData[name] = value;
        this.setState({
            formData
        });
    }

    renderTableData() {
        return this.state.pastPredictions.map((history, index) => {
            const {id, dateTime, features, prediction} = history
            return (
                <tr key={id}>
                    <td>{id}</td>
                    <td>{dateTime}</td>
                    <td>
                          <pre>{JSON.stringify(features, null, 2).slice(1,-1) }</pre>

                    </td>
                    <td>{prediction}</td>
                </tr>
            )
        })
    }

    renderTableHeader() {
        let header = Object.keys(this.state.pastPredictions[0])
        return header.map((key, index) => {
            return <th key={index}>{key.toUpperCase()}</th>
        })

    }

    handlePredictClick = (event) => {
        const formData = this.state.formData;
        this.setState({isLoading: true});
        fetch('http://127.0.0.1:5000/prediction/',
            {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(response => {
                this.setState({
                    result: response.result,
                    isLoading: false
                });
            });
    }


    handleCancelClick = (event) => {
        this.setState({result: "Lets predict another mushroom!"});
    }

    render() {
        const isLoading = this.state.isLoading;
        const formData = this.state.formData;
        const result = this.state.result;

        return (
            <Container>
                <div>
                    <h1 className="title">Can eat this mushroom?</h1>
                </div>
                <div className="content">
                    <h2 className="subtitle">Describe your mushroom</h2>
                    <Form>
                        <Form.Row>
                            <Form.Group as={Col}>
                                <Form.Label>Cap Shape</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.capShape}
                                    name="capShape"
                                    onChange={this.handleChange}>
                                    <option>Bell</option>
                                    <option>Conical</option>
                                    <option>Convex</option>
                                    <option>Flat</option>
                                    <option>Knobbed</option>
                                    <option>Sunken</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Cap Surface</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.capSurface}
                                    name="capSurface"
                                    onChange={this.handleChange}>
                                    <option>Fibrous</option>
                                    <option>Grooves</option>
                                    <option>Scaly</option>
                                    <option>Smooth</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Cap Colour</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.capColour}
                                    name="capColour"
                                    onChange={this.handleChange}>
                                    <option>Brown</option>
                                    <option>Buff</option>
                                    <option>Cinnamon</option>
                                    <option>Gray</option>
                                    <option>Green</option>
                                    <option>Pink</option>
                                    <option>Purple</option>
                                    <option>Red</option>
                                    <option>White</option>
                                    <option>Yellow</option>
                                </Form.Control>
                            </Form.Group>

                            <Form.Group as={Col}>
                                <Form.Label>Bruises</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.bruises}
                                    name="bruises"
                                    onChange={this.handleChange}>
                                    <option>Yes</option>
                                    <option>No</option>
                                </Form.Control>
                            </Form.Group>
                        </Form.Row>
                        <Form.Row>
                            <Form.Group as={Col}>
                                <Form.Label>Odour</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.odour}
                                    name="odour"
                                    onChange={this.handleChange}>
                                    <option>Almond</option>
                                    <option>Anise</option>
                                    <option>Creosote</option>
                                    <option>Fishy</option>
                                    <option>Foul</option>
                                    <option>Musty</option>
                                    <option>None</option>
                                    <option>Pungent</option>
                                    <option>Spicy</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Gill Attachment</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.gillAttachment}
                                    name="gillAttachment"
                                    onChange={this.handleChange}>
                                    <option>Attached</option>
                                    <option>Descending</option>
                                    <option>Free</option>
                                    <option>Notched</option>
                                </Form.Control>
                            </Form.Group>


                            <Form.Group as={Col}>
                                <Form.Label>Gill Spacing</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.gillSpacing}
                                    name="gillSpacing"
                                    onChange={this.handleChange}>
                                    <option>Close</option>
                                    <option>Crowded</option>
                                    <option>Distant</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Gill Size</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.gillSize}
                                    name="gillSize"
                                    onChange={this.handleChange}>
                                    <option>Broad</option>
                                    <option>Narrow</option>
                                </Form.Control>
                            </Form.Group>
                        </Form.Row>
                        <Form.Row>
                            <Form.Group as={Col}>
                                <Form.Label>Gill Colour</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.gillColour}
                                    name="gillColour"
                                    onChange={this.handleChange}>
                                    <option>Black</option>
                                    <option>Brown</option>
                                    <option>Buff</option>
                                    <option>Chocolate</option>
                                    <option>Gray</option>
                                    <option>Green</option>
                                    <option>Orange</option>
                                    <option>Pink</option>
                                    <option>Purple</option>
                                    <option>Red</option>
                                    <option>White</option>
                                    <option>Yellow</option>
                                </Form.Control>
                            </Form.Group>

                            <Form.Group as={Col}>
                                <Form.Label>Stalk Shape</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.stalkShape}
                                    name="stalkShape"
                                    onChange={this.handleChange}>
                                    <option>Enlarging</option>
                                    <option>Tapering</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Stalk Root</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.stalkRoot}
                                    name="stalkRoot"
                                    onChange={this.handleChange}>
                                    <option>Bulbous</option>
                                    <option>Club</option>
                                    <option>Cup</option>
                                    <option>Equal</option>
                                    <option>Rhizomorphs</option>
                                    <option>Rooted</option>
                                    <option>Missing</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Stalk Surface Above Ring</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.stalkSurfaceAboveRing}
                                    name="stalkSurfaceAboveRing"
                                    onChange={this.handleChange}>
                                    <option>Fibrous</option>
                                    <option>Scaly</option>
                                    <option>Silky</option>
                                    <option>Smooth</option>
                                </Form.Control>
                            </Form.Group>
                        </Form.Row>
                        <Form.Row>
                            <Form.Group as={Col}>
                                <Form.Label>Stalk Surface Below Ring</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.stalkSurfaceBelowRing}
                                    name="select13"
                                    onChange={this.handleChange}>
                                    <option>Fibrous</option>
                                    <option>Scaly</option>
                                    <option>Silky</option>
                                    <option>Smooth</option>
                                </Form.Control>
                            </Form.Group>

                            <Form.Group as={Col}>
                                <Form.Label>Stalk Colour Above Ring</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.stalkColourAboveRing}
                                    name="stalkColourAboveRing"
                                    onChange={this.handleChange}>
                                    <option>Brown</option>
                                    <option>Buff</option>
                                    <option>Cinnamon</option>
                                    <option>Gray</option>
                                    <option>Orange</option>
                                    <option>Pink</option>
                                    <option>Red</option>
                                    <option>White</option>
                                    <option>Yellow</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Stalk Colour Below Ring</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.stalkColourBelowRing}
                                    name="stalkColourBelowRing"
                                    onChange={this.handleChange}>
                                    <option>Brown</option>
                                    <option>Buff</option>
                                    <option>Cinnamon</option>
                                    <option>Gray</option>
                                    <option>Orange</option>
                                    <option>Pink</option>
                                    <option>Red</option>
                                    <option>White</option>
                                    <option>Yellow</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Veil Type</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.veilType}
                                    name="veilType"
                                    onChange={this.handleChange}>
                                    <option>Partial</option>
                                    <option>Universal</option>
                                </Form.Control>
                            </Form.Group>
                        </Form.Row>
                        <Form.Row>
                            <Form.Group as={Col}>
                                <Form.Label>Veil Colour</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.veilColour}
                                    name="veilColour"
                                    onChange={this.handleChange}>
                                    <option>Brown</option>
                                    <option>Orange</option>
                                    <option>White</option>
                                    <option>Yellow</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Ring Number</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.ringNumber}
                                    name="ringNumber"
                                    onChange={this.handleChange}>
                                    <option>None</option>
                                    <option>One</option>
                                    <option>Two</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Ring Type</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.ringType}
                                    name="ringType"
                                    onChange={this.handleChange}>
                                    <option>Cobwebby</option>
                                    <option>Evanescent</option>
                                    <option>Flaring</option>
                                    <option>Large</option>
                                    <option>None</option>
                                    <option>Pendant</option>
                                    <option>Sheathing</option>
                                    <option>Zone</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Spore Print Colour</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.sporePrintColour}
                                    name="sporePrintColour"
                                    onChange={this.handleChange}>
                                    <option>Black</option>
                                    <option>Brown</option>
                                    <option>Buff</option>
                                    <option>Chocolate</option>
                                    <option>Green</option>
                                    <option>Orange</option>
                                    <option>Purple</option>
                                    <option>White</option>
                                    <option>Yellow</option>
                                </Form.Control>
                            </Form.Group>
                        </Form.Row>
                        <Form.Row>
                            <Form.Group as={Col}>
                                <Form.Label>Population</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.population}
                                    name="population"
                                    onChange={this.handleChange}>
                                    <option>Abundant</option>
                                    <option>Clustered</option>
                                    <option>Numerous</option>
                                    <option>Scattered</option>
                                    <option>Several</option>
                                    <option>Solitary</option>
                                </Form.Control>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Label>Habitat</Form.Label>
                                <Form.Control
                                    as="select"
                                    value={formData.habitat}
                                    name="habitat"
                                    onChange={this.handleChange}>
                                    <option>Grasses</option>
                                    <option>Leaves</option>
                                    <option>Meadows</option>
                                    <option>Paths</option>
                                    <option>Urban</option>
                                    <option>Waste</option>
                                    <option>Woods</option>
                                </Form.Control>
                            </Form.Group>
                        </Form.Row>
                        <Row>
                            <Col>
                                <Button
                                    block
                                    variant="success"
                                    disabled={isLoading}
                                    onClick={!isLoading ? this.handlePredictClick : null}>
                                    {isLoading ? 'Making prediction' : 'Predict'}
                                </Button>
                            </Col>
                            <Col>
                                <Button
                                    block
                                    variant="danger"
                                    disabled={isLoading}
                                    onClick={this.handleCancelClick}>
                                    Try Another
                                </Button>
                            </Col>
                        </Row>
                    </Form>
                    {result === "" ? null :
                        (<Row>
                            <Col className="result-container">
                                <h5 id="result">{result}</h5>
                            </Col>
                        </Row>)
                    }
                </div>
                <div className="history">
                    <h2> Past predictions</h2>
                    <table id='historicalPredictions'>
                        <tbody>
                        <tr>{this.renderTableHeader()}</tr>
                        {this.renderTableData()}
                        </tbody>

                    </table>
                </div>
            </Container>
        );
    }
}

export default App;