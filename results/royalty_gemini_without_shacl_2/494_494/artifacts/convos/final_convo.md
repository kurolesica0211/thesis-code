================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Bernhard Prinz und Markgraf von Baden (born 27 May 1970), styled Margrave of Baden and Duke of Zähringen, is the head of the House of Baden since 29 December 2022 following the death of his father, Maximilian.
Early life and family

Bernhard was born at Schloss Salem in Salem, Baden-Württemberg, on 27 May 1970.
He is the eldest son of Maximilian, Margrave of Baden, and Archduchess Valerie of Austria (born 1941) and was styled as the heir of his father, Hereditary Prince of Baden.
His paternal grandparents were Berthold, Margrave of Baden, and Princess Theodora of Greece and Denmark, who was a sister of Prince Philip, Duke of Edinburgh.
His maternal grandparents were Archduke Hubert Salvator of Austria and Princess Rosemary of Salm-Salm.
Prince Bernhard manages the family estates, including Staufenberg Castle, and the margravial wineries dedicated to preserving the grape variety Müller-Thurgau.
Bernhard has close relations with the British royal family, and his granduncle, Prince Philip, Duke of Edinburgh, often came to Germany to shoot with the Baden family.
On 17 April 2021, Bernhard was one of only thirty mourners at Prince Philip's ceremonial funeral at St George's Chapel, Windsor Castle.
Bernhard, along with his cousins Philipp, Prince of Hohenlohe-Langenburg, and Donatus, Landgrave of Hesse, was chosen to represent the families of the Duke's late sisters who had been prevented from attending his wedding in 1947.
Bernhard and his wife and siblings later attended a service of thanksgiving for Prince Philip's life at Westminster Abbey on 29 March 2022.
On 30 March 2023, he and his wife attended a state banquet given by Frank-Walter Steinmeier, President of Germany, at Bellevue Palace during King Charles III and Queen Camilla's state visit to Germany.
On 29 December 2022, his father, Maximilian, died and Bernhard became head of the former grand ducal house of Baden.
Though royal and noble titles were abolished in Germany in 1919 when the Weimar Republic was proclaimed, he is sometimes styled and titled His Royal Highness The Margrave of Baden, Duke of Zähringen, by courtesy.
Prior to this, he was styled and titled His Grand Ducal Highness Hereditary Prince of Baden.
On 24 April 2025 the Margrave attended the funeral of Andreas, Prince of Saxe-Coburg and Gotha as the representative of Charles III.
Marriage and children

Bernhard married Stephanie Anne Kaul (born 27 June 1966), daughter of Christian Kaul and Hannelore Scheel, in a civil ceremony on 22 June 2001 and a religious ceremony the following day at Schloss Salem.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (89c55220-f176-40e2-8c8f-4dce28aae409)
 Call ID: 89c55220-f176-40e2-8c8f-4dce28aae409
  Args:
    type: :Man
    source: Bernhard_Prinz_von_Baden
  AssignClass (03ea6472-a43a-4463-802c-e43b556a16e4)
 Call ID: 03ea6472-a43a-4463-802c-e43b556a16e4
  Args:
    type: :Person
    source: Bernhard_Prinz_von_Baden
  AddLiteral (3fcb73d7-4c4f-471d-b79d-db7e7cb8993a)
 Call ID: 3fcb73d7-4c4f-471d-b79d-db7e7cb8993a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1970
    source: Bernhard_Prinz_von_Baden
  AssignClass (f3242ce3-566b-4b35-a1bb-1e7450f7100c)
 Call ID: f3242ce3-566b-4b35-a1bb-1e7450f7100c
  Args:
    type: :Man
    source: Maximilian_Markgraf_von_Baden
  AssignClass (bcb9fc3a-ea8d-43fd-b798-d028957f013b)
 Call ID: bcb9fc3a-ea8d-43fd-b798-d028957f013b
  Args:
    type: :Person
    source: Maximilian_Markgraf_von_Baden
  AssignClass (e5223d83-5132-4c35-93bc-a75f5b7f0f41)
 Call ID: e5223d83-5132-4c35-93bc-a75f5b7f0f41
  Args:
    type: :Woman
    source: Valerie_von_Oesterreich
  AssignClass (99778472-5057-42a8-8aa5-34ab3d22bfdd)
 Call ID: 99778472-5057-42a8-8aa5-34ab3d22bfdd
  Args:
    type: :Person
    source: Valerie_von_Oesterreich
  AddLiteral (967bb2d6-c178-4808-8a37-9fdc3dcb85b6)
 Call ID: 967bb2d6-c178-4808-8a37-9fdc3dcb85b6
  Args:
    source: Valerie_von_Oesterreich
    literal_value: 1941
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
  AddTriple (3d6c7642-8409-49c1-b77d-306e7ce9c1e5)
 Call ID: 3d6c7642-8409-49c1-b77d-306e7ce9c1e5
  Args:
    relation: :hasFather
    source: Bernhard_Prinz_von_Baden
    target: Maximilian_Markgraf_von_Baden
  AddTriple (81094cfe-dc61-4148-bc8e-998e8727709a)
 Call ID: 81094cfe-dc61-4148-bc8e-998e8727709a
  Args:
    target: Valerie_von_Oesterreich
    source: Bernhard_Prinz_von_Baden
    relation: :hasMother
  AddLiteral (7a9875b9-88e1-4646-ada4-4bb094f596df)
 Call ID: 7a9875b9-88e1-4646-ada4-4bb094f596df
  Args:
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    literal_value: 2022
    source: Maximilian_Markgraf_von_Baden
  AssignClass (ddbe866c-1411-4160-90ae-c5c613230658)
 Call ID: ddbe866c-1411-4160-90ae-c5c613230658
  Args:
    type: :Man
    source: Berthold_Markgraf_von_Baden
  AssignClass (400955c0-9f7a-477d-ba88-835edb745d3d)
 Call ID: 400955c0-9f7a-477d-ba88-835edb745d3d
  Args:
    type: :Person
    source: Berthold_Markgraf_von_Baden
  AssignClass (e67dd107-de49-492d-aebf-440278a51e06)
 Call ID: e67dd107-de49-492d-aebf-440278a51e06
  Args:
    type: :Woman
    source: Theodora_von_Griechenland_und_Daenemark
  AssignClass (744e2588-80e5-4931-be20-2844872c3c7e)
 Call ID: 744e2588-80e5-4931-be20-2844872c3c7e
  Args:
    type: :Person
    source: Theodora_von_Griechenland_und_Daenemark
  AddTriple (e9e839a7-8973-4c9e-b600-4ac2d8c4e38e)
 Call ID: e9e839a7-8973-4c9e-b600-4ac2d8c4e38e
  Args:
    relation: :hasFather
    target: Berthold_Markgraf_von_Baden
    source: Maximilian_Markgraf_von_Baden
  AddTriple (239c7f00-3ce1-4470-ade4-3c7fdbd21f88)
 Call ID: 239c7f00-3ce1-4470-ade4-3c7fdbd21f88
  Args:
    target: Theodora_von_Griechenland_und_Daenemark
    source: Maximilian_Markgraf_von_Baden
    relation: :hasMother
  AssignClass (680c7e35-018d-4231-b245-0fd337a253c5)
 Call ID: 680c7e35-018d-4231-b245-0fd337a253c5
  Args:
    type: :Man
    source: Hubert_Salvator_von_Oesterreich
  AssignClass (75303df3-c8a1-4845-9c60-ca062f25fe6a)
 Call ID: 75303df3-c8a1-4845-9c60-ca062f25fe6a
  Args:
    type: :Person
    source: Hubert_Salvator_von_Oesterreich
  AssignClass (dbeffcc0-4871-4c24-977e-65294aa2d7d2)
 Call ID: dbeffcc0-4871-4c24-977e-65294aa2d7d2
  Args:
    type: :Woman
    source: Rosemary_von_Salm-Salm
  AssignClass (996a6f9b-9224-4598-822c-f8d8d7efba29)
 Call ID: 996a6f9b-9224-4598-822c-f8d8d7efba29
  Args:
    type: :Person
    source: Rosemary_von_Salm-Salm
  AddTriple (e986aad8-611c-4759-8ad8-76d2386e66c3)
 Call ID: e986aad8-611c-4759-8ad8-76d2386e66c3
  Args:
    source: Valerie_von_Oesterreich
    target: Hubert_Salvator_von_Oesterreich
    relation: :hasFather
  AddTriple (39823876-fabb-416a-8202-5e94b5a0f0e5)
 Call ID: 39823876-fabb-416a-8202-5e94b5a0f0e5
  Args:
    target: Rosemary_von_Salm-Salm
    source: Valerie_von_Oesterreich
    relation: :hasMother
  AssignClass (8a3b632e-8610-4cf9-aa80-725fdcfa9281)
 Call ID: 8a3b632e-8610-4cf9-aa80-725fdcfa9281
  Args:
    type: :Woman
    source: Stephanie_Anne_Kaul
  AssignClass (0e6b3ff1-514b-44f7-9b5a-22118a40f4f2)
 Call ID: 0e6b3ff1-514b-44f7-9b5a-22118a40f4f2
  Args:
    type: :Person
    source: Stephanie_Anne_Kaul
  AddLiteral (aa72d257-8a7f-41f8-a627-2058a563c4d9)
 Call ID: aa72d257-8a7f-41f8-a627-2058a563c4d9
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1966
    source: Stephanie_Anne_Kaul
  AddTriple (da394d8d-b198-4790-9889-08f59deaf1e0)
 Call ID: da394d8d-b198-4790-9889-08f59deaf1e0
  Args:
    source: Bernhard_Prinz_von_Baden
    target: Stephanie_Anne_Kaul
    relation: :hasRelation
  AddLiteral (77481274-e102-4952-91fc-f83540b68418)
 Call ID: 77481274-e102-4952-91fc-f83540b68418
  Args:
    literal_value: 2001
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    source: Bernhard_Prinz_von_Baden
  AssignClass (7af25af1-1c63-4a5f-9e08-fc7be55be525)
 Call ID: 7af25af1-1c63-4a5f-9e08-fc7be55be525
  Args:
    type: :Man
    source: Christian_Kaul
  AssignClass (97b354b5-1751-4bbb-b1ae-60516b0e54ac)
 Call ID: 97b354b5-1751-4bbb-b1ae-60516b0e54ac
  Args:
    type: :Person
    source: Christian_Kaul
  AssignClass (1dc7428d-2648-4034-8aa9-5231bfaed3f8)
 Call ID: 1dc7428d-2648-4034-8aa9-5231bfaed3f8
  Args:
    type: :Woman
    source: Hannelore_Scheel
  AssignClass (09fa8786-5f1d-4ed0-9762-7315991f9458)
 Call ID: 09fa8786-5f1d-4ed0-9762-7315991f9458
  Args:
    type: :Person
    source: Hannelore_Scheel
  AddTriple (be961291-d26e-4bc0-a48c-30aa65b58343)
 Call ID: be961291-d26e-4bc0-a48c-30aa65b58343
  Args:
    target: Christian_Kaul
    source: Stephanie_Anne_Kaul
    relation: :hasFather
  AddTriple (d9fa47e4-833f-4f08-8367-912362f0c971)
 Call ID: d9fa47e4-833f-4f08-8367-912362f0c971
  Args:
    target: Hannelore_Scheel
    source: Stephanie_Anne_Kaul
    relation: :hasMother
  Finish (0925b142-2a3e-4713-ad2b-06d9d257325e)
 Call ID: 0925b142-2a3e-4713-ad2b-06d9d257325e
  Args: