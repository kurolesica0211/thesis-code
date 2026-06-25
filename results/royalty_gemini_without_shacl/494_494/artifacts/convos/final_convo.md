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
  AssignClass (2e9c0034-c2a5-4456-ba54-0304f2f6dfc8)
 Call ID: 2e9c0034-c2a5-4456-ba54-0304f2f6dfc8
  Args:
    source: Bernhard
    type: :Man
  AssignClass (e5dd4c3d-824e-472a-a376-9973b9b07acf)
 Call ID: e5dd4c3d-824e-472a-a376-9973b9b07acf
  Args:
    type: :Person
    source: Bernhard
  AddLiteral (0b8cd71c-d1cf-4e83-a564-c3da24ef9e94)
 Call ID: 0b8cd71c-d1cf-4e83-a564-c3da24ef9e94
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1970
    source: Bernhard
  AssignClass (b165a0ba-613f-4f10-b832-a7a2a66c5469)
 Call ID: b165a0ba-613f-4f10-b832-a7a2a66c5469
  Args:
    source: Maximilian
    type: :Man
  AssignClass (b76b9cec-b738-4ce2-9b4a-a45d7fd0abe2)
 Call ID: b76b9cec-b738-4ce2-9b4a-a45d7fd0abe2
  Args:
    type: :Person
    source: Maximilian
  AddTriple (863c9aa2-5b54-4a37-911c-10dbaee63815)
 Call ID: 863c9aa2-5b54-4a37-911c-10dbaee63815
  Args:
    relation: :hasFather
    target: Maximilian
    source: Bernhard
  AssignClass (66447ecb-7cab-48c4-ab52-39bb3de7a468)
 Call ID: 66447ecb-7cab-48c4-ab52-39bb3de7a468
  Args:
    source: Valerie_of_Austria
    type: :Woman
  AssignClass (b97e868c-04d3-4afe-b21d-58d91757a3d8)
 Call ID: b97e868c-04d3-4afe-b21d-58d91757a3d8
  Args:
    source: Valerie_of_Austria
    type: :Person
  AddLiteral (4f41b741-93f1-4359-8dae-762f91c58e13)
 Call ID: 4f41b741-93f1-4359-8dae-762f91c58e13
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Valerie_of_Austria
    literal_value: 1941
  AddTriple (8c949e07-1f38-4842-8c7b-e03dfa07ff0d)
 Call ID: 8c949e07-1f38-4842-8c7b-e03dfa07ff0d
  Args:
    relation: :hasMother
    source: Bernhard
    target: Valerie_of_Austria
  AssignClass (22daef87-7282-4101-abb8-a2296299482d)
 Call ID: 22daef87-7282-4101-abb8-a2296299482d
  Args:
    source: Berthold
    type: :Man
  AssignClass (00c368fa-f4bc-4507-b372-2228767768b8)
 Call ID: 00c368fa-f4bc-4507-b372-2228767768b8
  Args:
    type: :Person
    source: Berthold
  AddTriple (e6baf660-b8dd-437a-872c-6487c13a6d1b)
 Call ID: e6baf660-b8dd-437a-872c-6487c13a6d1b
  Args:
    relation: :hasFather
    target: Berthold
    source: Maximilian
  AssignClass (477afabc-cdd8-4b96-bb7f-54c300978547)
 Call ID: 477afabc-cdd8-4b96-bb7f-54c300978547
  Args:
    source: Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (cdee47cd-ff40-4464-a3e6-dc8aebedda2d)
 Call ID: cdee47cd-ff40-4464-a3e6-dc8aebedda2d
  Args:
    type: :Person
    source: Theodora_of_Greece_and_Denmark
  AddTriple (544eda35-37c4-4107-8f98-d1466aa2db92)
 Call ID: 544eda35-37c4-4107-8f98-d1466aa2db92
  Args:
    target: Theodora_of_Greece_and_Denmark
    source: Maximilian
    relation: :hasMother
  AssignClass (fb20d1ef-cf9e-4db7-b4cf-08ff028d9e3f)
 Call ID: fb20d1ef-cf9e-4db7-b4cf-08ff028d9e3f
  Args:
    type: :Man
    source: Hubert_Salvator_of_Austria
  AssignClass (435c0e05-0760-40e3-992d-dcd3fc7ccb25)
 Call ID: 435c0e05-0760-40e3-992d-dcd3fc7ccb25
  Args:
    source: Hubert_Salvator_of_Austria
    type: :Person
  AddTriple (c13b24d3-f047-4515-9c87-9508d86f5e12)
 Call ID: c13b24d3-f047-4515-9c87-9508d86f5e12
  Args:
    source: Valerie_of_Austria
    target: Hubert_Salvator_of_Austria
    relation: :hasFather
  AssignClass (d97f78c5-a5f8-4c09-aa84-e09cd101a1c4)
 Call ID: d97f78c5-a5f8-4c09-aa84-e09cd101a1c4
  Args:
    source: Rosemary_of_Salm-Salm
    type: :Woman
  AssignClass (7ecd88db-84cf-48de-85d1-01c6263a1b31)
 Call ID: 7ecd88db-84cf-48de-85d1-01c6263a1b31
  Args:
    source: Rosemary_of_Salm-Salm
    type: :Person
  AddTriple (9d3a42e1-4256-4b79-ae05-b1a8f056a402)
 Call ID: 9d3a42e1-4256-4b79-ae05-b1a8f056a402
  Args:
    relation: :hasMother
    source: Valerie_of_Austria
    target: Rosemary_of_Salm-Salm
  AssignClass (d1ae01f5-faa9-4b6d-be28-bdc761aa850e)
 Call ID: d1ae01f5-faa9-4b6d-be28-bdc761aa850e
  Args:
    source: Stephanie_Anne_Kaul
    type: :Woman
  AssignClass (52bf9847-bf7c-46a3-bac7-db0669e2c751)
 Call ID: 52bf9847-bf7c-46a3-bac7-db0669e2c751
  Args:
    type: :Person
    source: Stephanie_Anne_Kaul
  AddLiteral (6ee494ec-8915-4728-b1c7-495a61f26cfc)
 Call ID: 6ee494ec-8915-4728-b1c7-495a61f26cfc
  Args:
    literal_type: xsd:integer
    literal_value: 1966
    source: Stephanie_Anne_Kaul
    relation: :hasBirthYear
  AddTriple (31a35357-29dd-4460-b9fe-6f9cfd67afb3)
 Call ID: 31a35357-29dd-4460-b9fe-6f9cfd67afb3
  Args:
    relation: :hasRelation
    source: Bernhard
    target: Stephanie_Anne_Kaul
  AddLiteral (38517741-c55d-4dfe-800e-e00fa01d901b)
 Call ID: 38517741-c55d-4dfe-800e-e00fa01d901b
  Args:
    literal_value: 2001
    source: Bernhard
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (ce189496-065f-47a8-8fee-f4476908ba36)
 Call ID: ce189496-065f-47a8-8fee-f4476908ba36
  Args:
    source: Christian_Kaul
    type: :Man
  AssignClass (a8f897b2-376d-4f01-98bb-649f268e8bac)
 Call ID: a8f897b2-376d-4f01-98bb-649f268e8bac
  Args:
    source: Christian_Kaul
    type: :Person
  AddTriple (26f8740f-7ba5-45f8-8463-d15ea7f0c989)
 Call ID: 26f8740f-7ba5-45f8-8463-d15ea7f0c989
  Args:
    relation: :hasFather
    source: Stephanie_Anne_Kaul
    target: Christian_Kaul
  AssignClass (42f1bc57-fe0b-4761-838a-afa3b2371266)
 Call ID: 42f1bc57-fe0b-4761-838a-afa3b2371266
  Args:
    source: Hannelore_Scheel
    type: :Woman
  AssignClass (eae00645-7d10-484a-a0c6-7294a5f6a4e6)
 Call ID: eae00645-7d10-484a-a0c6-7294a5f6a4e6
  Args:
    source: Hannelore_Scheel
    type: :Person
  AddTriple (c32a97f7-8e02-4ded-8e73-946c4749bed1)
 Call ID: c32a97f7-8e02-4ded-8e73-946c4749bed1
  Args:
    target: Hannelore_Scheel
    source: Stephanie_Anne_Kaul
    relation: :hasMother
  Finish (535c5404-35ba-4eef-aab5-35bd4f7f98c0)
 Call ID: 535c5404-35ba-4eef-aab5-35bd4f7f98c0
  Args: