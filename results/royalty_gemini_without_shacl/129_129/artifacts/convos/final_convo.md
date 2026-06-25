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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Princess Carolina of Bourbon-Parma, Marchioness of Sala (born 23 June 1974), is the fourth and youngest child of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
She is a member of the House of Bourbon-Parma as well an extended member of the Dutch royal family.
Per a 1996 royal decree issued by Queen Beatrix, she is entitled to the style and title Her Royal Highness Princess Maria Carolina de Bourbon de Parme in The Netherlands as a member of the extended royal family.
Early life

Princess Carolina was born at 23 June 1974 in Nijmegen.
She has two older brothers, Prince Carlos, the head of the House of Bourbon-Parma, and Prince Jaime.
She also has one older sister, Princess Margarita.
She was baptised at the Castle of Lignières in France with Prince Claus of the Netherlands, Princess Christina of the Netherlands and Princess Marie des Neiges of Bourbon-Parma as her godparents.
She moved together with her mother and her brothers and sister to Soest, Netherlands, nearby the then residence of her grandparents the former Queen of the Netherlands Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
Education and career

Princess Carolina studied political science at University of Amsterdam and Harvard University, and also has an M.Sc.
Marriage

On 9 January 2012, it was announced that Princess Carolina would marry Albert Alphons Ludgerus Brenninkmeijer (born 16 May 1974), a member of the wealthy Brenninkmeijer family.
The princess has been seen regularly at important events of the royal house of the Netherlands.
In 2001 she was one of the maids of honor at the wedding of Prince Constantijn and Petra Laurentien Brinkhorst; and during the baptism of their daughter, Countess Eloise of Orange-Nassau, she was the godmother of the child.
She was a witness at the church wedding of her cousin Prince Floris of Orange-Nassau, van Vollenhoven, and in 2010, was named as the godmother of Floris' second child, Eliane.


Titles, styles and honours

Already a ducal princess from birth, her father bestowed the substantive title Marchesa di Sala (Marchioness of Sala) upon her on 2 September 1996.
In 1996 she was incorporated into the Dutch nobility by her aunt Queen Beatrix, with the highest title of nobility Prinses de Bourbon de Parme (Princess of Bourbon-Parma) and styled Hare Koninklijke Hoogheid (Her Royal Highness).
She does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a granddaughter of Queen Juliana and first cousin of the present King Willem-Alexander, she is officially a member of the more extended Dutch royal family.
Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (c859e415-a551-4416-9a62-4e736d55dd42)
 Call ID: c859e415-a551-4416-9a62-4e736d55dd42
  Args:
    source: :Princess_Carolina_of_Bourbon-Parma
    type: :Woman
  AssignClass (fb4b913a-db26-4ed5-85fa-c4d57a1fa140)
 Call ID: fb4b913a-db26-4ed5-85fa-c4d57a1fa140
  Args:
    source: :Princess_Irene_of_the_Netherlands
    type: :Woman
  AssignClass (485fbe7f-89c7-4b7a-8c8d-c26cb19fc5dc)
 Call ID: 485fbe7f-89c7-4b7a-8c8d-c26cb19fc5dc
  Args:
    source: :Carlos_Hugo_Duke_of_Parma
    type: :Man
  AddTriple (cedf66ab-73b2-4c83-94a7-72df03957292)
 Call ID: cedf66ab-73b2-4c83-94a7-72df03957292
  Args:
    target: :Princess_Irene_of_the_Netherlands
    relation: :isDaughterOf
    source: :Princess_Carolina_of_Bourbon-Parma
  AddTriple (f9960ee8-f242-4c9a-b7be-cc20a212b642)
 Call ID: f9960ee8-f242-4c9a-b7be-cc20a212b642
  Args:
    relation: :isDaughterOf
    source: :Princess_Carolina_of_Bourbon-Parma
    target: :Carlos_Hugo_Duke_of_Parma
  AddLiteral (bf3be2a8-b258-4e1d-bb69-0ea4a8340e0f)
 Call ID: bf3be2a8-b258-4e1d-bb69-0ea4a8340e0f
  Args:
    literal_type: xsd:date
    relation: :hasBirthYear
    literal_value: 1974-06-23
    source: :Princess_Carolina_of_Bourbon-Parma
  AssignClass (791bd284-0a29-4d1a-92e4-a4ffd686d87b)
 Call ID: 791bd284-0a29-4d1a-92e4-a4ffd686d87b
  Args:
    source: :Prince_Carlos
    type: :Man
  AssignClass (fbd6000c-9565-4e2c-8e2f-d8ea0f7b43a1)
 Call ID: fbd6000c-9565-4e2c-8e2f-d8ea0f7b43a1
  Args:
    source: :Prince_Jaime
    type: :Man
  AssignClass (9e7b064f-7c36-4080-8266-4a04c24d3be7)
 Call ID: 9e7b064f-7c36-4080-8266-4a04c24d3be7
  Args:
    source: :Princess_Margarita
    type: :Woman
  AddTriple (33682550-9674-4398-ab0f-e48f8a9a3eec)
 Call ID: 33682550-9674-4398-ab0f-e48f8a9a3eec
  Args:
    source: :Princess_Carolina_of_Bourbon-Parma
    relation: :isSiblingOf
    target: :Prince_Carlos
  AddTriple (c0baa7ec-779b-40c5-826a-898e650724ba)
 Call ID: c0baa7ec-779b-40c5-826a-898e650724ba
  Args:
    target: :Prince_Jaime
    source: :Princess_Carolina_of_Bourbon-Parma
    relation: :isSiblingOf
  AddTriple (ce3a389d-3d8e-4e2c-bd90-900a8c5d4cf1)
 Call ID: ce3a389d-3d8e-4e2c-bd90-900a8c5d4cf1
  Args:
    target: :Princess_Margarita
    source: :Princess_Carolina_of_Bourbon-Parma
    relation: :isSiblingOf
  AssignClass (fce18cdc-e893-4305-a36b-d3b4969d1a3a)
 Call ID: fce18cdc-e893-4305-a36b-d3b4969d1a3a
  Args:
    source: :Albert_Alphons_Ludgerus_Brenninkmeijer
    type: :Man
  AddLiteral (c66d7b34-522c-4e63-8c9b-079c1e6d1391)
 Call ID: c66d7b34-522c-4e63-8c9b-079c1e6d1391
  Args:
    literal_type: xsd:date
    relation: :hasBirthYear
    literal_value: 1974-05-16
    source: :Albert_Alphons_Ludgerus_Brenninkmeijer
  AssignClass (2ac6e6e4-7240-4b24-9e2d-1890cc59f620)
 Call ID: 2ac6e6e4-7240-4b24-9e2d-1890cc59f620
  Args:
    source: :Queen_Juliana_of_the_Netherlands
    type: :Woman
  AssignClass (fe66cce8-2fa2-4a05-9519-a7dd7e0eadbc)
 Call ID: fe66cce8-2fa2-4a05-9519-a7dd7e0eadbc
  Args:
    source: :Prince_Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AddTriple (36ae3c53-5b21-4a60-a45d-ca42cf4ba4f0)
 Call ID: 36ae3c53-5b21-4a60-a45d-ca42cf4ba4f0
  Args:
    source: :Queen_Juliana_of_the_Netherlands
    relation: :isParentOf
    target: :Princess_Irene_of_the_Netherlands
  AddTriple (328a91fe-958f-485c-abb4-ad698e866806)
 Call ID: 328a91fe-958f-485c-abb4-ad698e866806
  Args:
    source: :Prince_Bernhard_of_Lippe-Biesterfeld
    relation: :isParentOf
    target: :Princess_Irene_of_the_Netherlands
  Finish (02c2abe8-994b-4204-b730-c980fd9ace74)
 Call ID: 02c2abe8-994b-4204-b730-c980fd9ace74
  Args: