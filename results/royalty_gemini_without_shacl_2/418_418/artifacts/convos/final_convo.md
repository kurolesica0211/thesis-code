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
Prince Philippe, Duke of Orléans (French: Louis Philippe Robert; 6 February 1869 – 28 March 1926) was the Orléanist pretender to the throne of France from 1894 to 1926 as Philippe VIII.
Early life

Philippe was born at York House, Twickenham, near London, the son of Philippe, Count of Paris, by his wife (and first cousin), Princess Isabelle of Orléans.
He was baptised with the names Louis-Philippe-Robert, and was called Philippe.
His family lived in the United Kingdom from the abdication and banishment of his great-grandfather Louis Philippe I, King of the French, in 1848, and returned to France in 1871 following the fall of the Second French Empire.
However, they again took refuge in England in 1886, when the French Republic exiled them following the wedding in Paris of Philippe's sister Amélie of Orléans to Crown Prince Carlos of Portugal.
Returning therefore to France in 1871 with his parents, Philippe was educated at home at the Château d'Eu and at the Collège Stanislas de Paris.
In 1880 Philippe's father granted him the title Duc d'Orléans.
Military career

Philippe began his military education at the École spéciale militaire de Saint-Cyr.
In October 1889, Philippe went to Switzerland to complete a course in military theory.
While there he fathered a son, Philippe Debien, by Nina, an actress working in the casino at Lausanne.
Drawn to explore the "unknown", Philippe asked Prince George, Duke of Cambridge, to send him to a military post in the Himalayas.
While in the East, he undertook a hunting and exploratory expedition in Nepal with his cousin Prince Henri of Orléans, went mountain-climbing in Tibet, and visited Afghanistan, Ceylon, and the Persian Gulf, before being posted back to Britain.
Prior to his imprisonment in France, Philippe had been unofficially engaged to his first cousin Princess Marguerite of Orléans, but the engagement was cancelled when Philippe's involvement with the Australian opera singer Nellie Melba was revealed.
Armstrong filed for divorce from Melba on the grounds of adultery, naming Philippe as co-respondent; the case was eventually dropped.
In September 1890, Philippe accompanied his father on a two-month trip to the United States and Canada.
On 12 November 1890, while in Philadelphia, Philippe joined the Pennsylvania Commandery of the Military Order of the Loyal Legion of the United States (MOLLUS) - a military society composed of officers who had served the Union in the American Civil War and their descendants - by right of his father's service in the Union Army.
In December 1890, Philippe applied unsuccessfully to serve in the Russian Army.
In March 1894, Philippe went to Egypt and Palestine with his sister Hélène, Duchess of Aosta.
Claimant to the defunct throne

Upon the death of his father on 8 September 1894, Philippe became the Orléanist claimant to the defunct French throne.
He was known to monarchists as Philippe VIII.
In October 1895, Philippe was named as co-respondent in the divorce case of Woolston v. Woolston.
Unlike his great grandfather, Louis Philippe I, Philippe claimed grand mastership of the Order of the Holy Spirit as intrinsic to his dynastic claim to the throne, and sometimes wore the breast star of the order.
On 5 November 1896, in Vienna, Philippe married Archduchess Maria Dorothea of Austria (1867–1932), a daughter of Archduke Joseph Karl of Austria, Palatine of Hungary, and granddaughter of Princess Clémentine of Orléans, as well as a niece of Marie Henriette of Austria, Queen Consort of the Belgians.
While travelling in Geneva in 1898, Philippe narrowly missed being assassinated by Luigi Lucheni, an anarchist, who vowed to kill the next member of a royal family that he saw.
He explored parts of the northeastern coast of Greenland, Denmark, in 1905 during his Duke of Orléans Arctic Expedition on ship Belgica.
Philippe continued to reside in the United Kingdom until 1912, when he moved his primary residence to Belgium.
In 1914, Philippe and his wife Maria Dorothea were legally separated.
At the outbreak of the First World War, Philippe again tried unsuccessfully to join the French army.
In 1926, Philippe died of pneumonia at the Palais d'Orléans in Palermo, Sicily, Italy.
Having no legitimate issue, he was succeeded as pretender to the defunct throne of France by his cousin and brother in law, Jean, Duke of Guise.
Publications

Philippe wrote a number of works based on his many travels: 


He also published a collection of the papers of his father and of the Henri, comte de Chambord:
Honours

In popular culture

Duke Philippe of Orleans briefly appears in an urban fantasy novel for children, The Master Key (1901) by L. Frank Baum.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (89834e38-a38f-4a92-b79f-e2932a41b5e2)
 Call ID: 89834e38-a38f-4a92-b79f-e2932a41b5e2
  Args:
    source: Philippe_Duke_of_Orleans
    type: :Man
  AssignClass (0df6d8a6-9bb6-4575-b718-a0b98791c3e2)
 Call ID: 0df6d8a6-9bb6-4575-b718-a0b98791c3e2
  Args:
    type: :Person
    source: Philippe_Duke_of_Orleans
  AddLiteral (2d5c4ead-8277-4e5e-a642-0e75e7209032)
 Call ID: 2d5c4ead-8277-4e5e-a642-0e75e7209032
  Args:
    literal_value: 1869
    source: Philippe_Duke_of_Orleans
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (bda9939d-75b0-4f33-925f-2e3129536223)
 Call ID: bda9939d-75b0-4f33-925f-2e3129536223
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Philippe_Duke_of_Orleans
    literal_value: 1926
  AddLiteral (87e05cb3-9fbf-4d99-a5f4-9769d77df742)
 Call ID: 87e05cb3-9fbf-4d99-a5f4-9769d77df742
  Args:
    literal_value: Louis Philippe Robert
    source: Philippe_Duke_of_Orleans
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (abb529c6-e579-49fb-b0b2-aabc7c0780aa)
 Call ID: abb529c6-e579-49fb-b0b2-aabc7c0780aa
  Args:
    source: Philippe_Duke_of_Orleans
    literal_value: Philippe VIII
    relation: :knownAs
    literal_type: xsd:string
  AssignClass (c6aac344-ac8d-4bb7-8cf9-b36b4c98c824)
 Call ID: c6aac344-ac8d-4bb7-8cf9-b36b4c98c824
  Args:
    source: Philippe_Count_of_Paris
    type: :Man
  AssignClass (786cc716-03c5-4d25-9294-ef45c91d27b9)
 Call ID: 786cc716-03c5-4d25-9294-ef45c91d27b9
  Args:
    source: Philippe_Count_of_Paris
    type: :Person
  AssignClass (8900cd3a-dc15-433f-98f7-4eb95380062c)
 Call ID: 8900cd3a-dc15-433f-98f7-4eb95380062c
  Args:
    source: Princess_Isabelle_of_Orleans
    type: :Woman
  AssignClass (10ba1112-9723-4bdd-bb36-1609234c437d)
 Call ID: 10ba1112-9723-4bdd-bb36-1609234c437d
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orleans
  AddTriple (0ec979b3-a89f-423c-8e17-2ba1889061eb)
 Call ID: 0ec979b3-a89f-423c-8e17-2ba1889061eb
  Args:
    relation: :hasFather
    target: Philippe_Count_of_Paris
    source: Philippe_Duke_of_Orleans
  AddTriple (71b2f7ce-042e-4668-bfaa-dda6da27663e)
 Call ID: 71b2f7ce-042e-4668-bfaa-dda6da27663e
  Args:
    target: Princess_Isabelle_of_Orleans
    source: Philippe_Duke_of_Orleans
    relation: :hasMother
  AssignClass (208df95f-8667-4507-82ad-215389ff61da)
 Call ID: 208df95f-8667-4507-82ad-215389ff61da
  Args:
    source: Amelie_of_Orleans
    type: :Woman
  AssignClass (912adf36-4c4f-4e2f-a60e-0a039ee51ae6)
 Call ID: 912adf36-4c4f-4e2f-a60e-0a039ee51ae6
  Args:
    source: Amelie_of_Orleans
    type: :Person
  AddTriple (7aa13c35-7685-49ff-be07-4eabc6460b95)
 Call ID: 7aa13c35-7685-49ff-be07-4eabc6460b95
  Args:
    target: Philippe_Duke_of_Orleans
    source: Amelie_of_Orleans
    relation: :isSisterOf
  AssignClass (3460a032-43c7-4e86-9776-6edb45e0deb0)
 Call ID: 3460a032-43c7-4e86-9776-6edb45e0deb0
  Args:
    source: Philippe_Debien
    type: :Man
  AssignClass (5aeb1c0b-9756-4505-964e-6d5bd64cfb9b)
 Call ID: 5aeb1c0b-9756-4505-964e-6d5bd64cfb9b
  Args:
    type: :Person
    source: Philippe_Debien
  AssignClass (ffa941c8-7080-4653-9136-648e9a49827f)
 Call ID: ffa941c8-7080-4653-9136-648e9a49827f
  Args:
    source: Nina
    type: :Woman
  AssignClass (a6afe91e-2795-464a-99b3-cc9dd5f7c3eb)
 Call ID: a6afe91e-2795-464a-99b3-cc9dd5f7c3eb
  Args:
    source: Nina
    type: :Person
  AddTriple (aa358c9b-e228-455a-907c-7fdfab8e5002)
 Call ID: aa358c9b-e228-455a-907c-7fdfab8e5002
  Args:
    target: Philippe_Debien
    source: Philippe_Duke_of_Orleans
    relation: :isFatherOf
  AddTriple (7ffeb195-db01-4121-aa71-b8e8b9be4c83)
 Call ID: 7ffeb195-db01-4121-aa71-b8e8b9be4c83
  Args:
    target: Philippe_Debien
    source: Nina
    relation: :isMotherOf
  AssignClass (912c904b-fad7-4fff-abb0-d7c81b9c4b09)
 Call ID: 912c904b-fad7-4fff-abb0-d7c81b9c4b09
  Args:
    source: Princess_Marguerite_of_Orleans
    type: :Woman
  AssignClass (6490de7f-1a25-4506-a357-58defda10f0c)
 Call ID: 6490de7f-1a25-4506-a357-58defda10f0c
  Args:
    type: :Person
    source: Princess_Marguerite_of_Orleans
  AssignClass (f7b9500c-29d1-4d3b-8f21-4663cdffc425)
 Call ID: f7b9500c-29d1-4d3b-8f21-4663cdffc425
  Args:
    type: :Woman
    source: Helene_Duchess_of_Aosta
  AssignClass (5009c655-1811-4061-a9f0-7428aad24921)
 Call ID: 5009c655-1811-4061-a9f0-7428aad24921
  Args:
    source: Helene_Duchess_of_Aosta
    type: :Person
  AddTriple (655d38a1-253b-4e1f-bcf1-1829ee6c42a2)
 Call ID: 655d38a1-253b-4e1f-bcf1-1829ee6c42a2
  Args:
    target: Philippe_Duke_of_Orleans
    source: Helene_Duchess_of_Aosta
    relation: :isSisterOf
  AssignClass (4740ce59-2d65-4d67-b96d-43016bbd03e4)
 Call ID: 4740ce59-2d65-4d67-b96d-43016bbd03e4
  Args:
    type: :Woman
    source: Archduchess_Maria_Dorothea_of_Austria
  AssignClass (a48526f2-fe35-45bc-8a76-27be3600984a)
 Call ID: a48526f2-fe35-45bc-8a76-27be3600984a
  Args:
    type: :Person
    source: Archduchess_Maria_Dorothea_of_Austria
  AddLiteral (c9779251-9be2-45af-81c8-33f60fc40277)
 Call ID: c9779251-9be2-45af-81c8-33f60fc40277
  Args:
    source: Philippe_Duke_of_Orleans
    literal_value: 1896
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (cf2a2a98-427e-44f0-b604-09663c53eb93)
 Call ID: cf2a2a98-427e-44f0-b604-09663c53eb93
  Args:
    relation: :hasRelation
    source: Philippe_Duke_of_Orleans
    target: Archduchess_Maria_Dorothea_of_Austria
  AssignClass (c7d37aea-6ec6-47f7-b0c3-f91a18907f3f)
 Call ID: c7d37aea-6ec6-47f7-b0c3-f91a18907f3f
  Args:
    type: :Man
    source: Archduke_Joseph_Karl_of_Austria
  AssignClass (f7bfcf7b-5e08-43c3-bd31-157e38e9c37f)
 Call ID: f7bfcf7b-5e08-43c3-bd31-157e38e9c37f
  Args:
    source: Archduke_Joseph_Karl_of_Austria
    type: :Person
  AddTriple (2833ffed-9e05-4596-8a04-1e5089bd2a57)
 Call ID: 2833ffed-9e05-4596-8a04-1e5089bd2a57
  Args:
    relation: :hasFather
    source: Archduchess_Maria_Dorothea_of_Austria
    target: Archduke_Joseph_Karl_of_Austria
  AssignClass (a149f7d2-1376-48e8-9790-a5580a998e00)
 Call ID: a149f7d2-1376-48e8-9790-a5580a998e00
  Args:
    source: Princess_Clementine_of_Orleans
    type: :Woman
  AssignClass (14f3b07e-9861-479e-868e-0bb113100350)
 Call ID: 14f3b07e-9861-479e-868e-0bb113100350
  Args:
    source: Princess_Clementine_of_Orleans
    type: :Person
  AssignClass (5291d55a-fe54-442a-8ad6-9901ff2222fe)
 Call ID: 5291d55a-fe54-442a-8ad6-9901ff2222fe
  Args:
    source: Jean_Duke_of_Guise
    type: :Man
  AssignClass (455fb721-d6da-4b62-a0e8-f405bc50b273)
 Call ID: 455fb721-d6da-4b62-a0e8-f405bc50b273
  Args:
    type: :Person
    source: Jean_Duke_of_Guise
  AddTriple (263d6a71-12da-474f-9deb-338bb55376de)
 Call ID: 263d6a71-12da-474f-9deb-338bb55376de
  Args:
    source: Jean_Duke_of_Guise
    target: Philippe_Duke_of_Orleans
    relation: :isBrotherOf
  Finish (71ab898a-4b42-4ce6-b925-bee0c3a9efc8)
 Call ID: 71ab898a-4b42-4ce6-b925-bee0c3a9efc8
  Args: