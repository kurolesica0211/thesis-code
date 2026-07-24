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
  AssignClass (518b7fa8-18d8-4639-99cd-e5849eb4be6b)
 Call ID: 518b7fa8-18d8-4639-99cd-e5849eb4be6b
  Args:
    type: :Woman
    source: Princess_Carolina_of_Bourbon-Parma
  AssignClass (808a94de-8505-452f-8018-b748fd2d9678)
 Call ID: 808a94de-8505-452f-8018-b748fd2d9678
  Args:
    source: Princess_Irene_of_the_Netherlands
    type: :Woman
  AssignClass (c1f20328-7d45-4252-a533-2a18b626d4b4)
 Call ID: c1f20328-7d45-4252-a533-2a18b626d4b4
  Args:
    source: Carlos_Hugo_Duke_of_Parma
    type: :Man
  AddTriple (c2b13069-279e-4fb4-a232-11b9915077ea)
 Call ID: c2b13069-279e-4fb4-a232-11b9915077ea
  Args:
    source: Princess_Carolina_of_Bourbon-Parma
    target: Princess_Irene_of_the_Netherlands
    relation: :isChildOf
  AddTriple (ec91080b-b33a-42a7-a444-39132b8fa43b)
 Call ID: ec91080b-b33a-42a7-a444-39132b8fa43b
  Args:
    relation: :isChildOf
    source: Princess_Carolina_of_Bourbon-Parma
    target: Carlos_Hugo_Duke_of_Parma
  AddLiteral (9ea9eee4-bbe7-4405-8b6b-57e16d46af26)
 Call ID: 9ea9eee4-bbe7-4405-8b6b-57e16d46af26
  Args:
    literal_value: 1974
    source: Princess_Carolina_of_Bourbon-Parma
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (fac09527-68e1-4c11-ab9c-cfcf2681ef49)
 Call ID: fac09527-68e1-4c11-ab9c-cfcf2681ef49
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon-Parma
  AssignClass (a48dd42a-982a-4cb2-89e7-58c71f21aa65)
 Call ID: a48dd42a-982a-4cb2-89e7-58c71f21aa65
  Args:
    type: :Man
    source: Prince_Jaime_of_Bourbon-Parma
  AssignClass (642b74a7-c6e3-4d59-ac90-c142e0232421)
 Call ID: 642b74a7-c6e3-4d59-ac90-c142e0232421
  Args:
    source: Princess_Margarita_of_Bourbon-Parma
    type: :Woman
  AddTriple (cc9370f2-e6ca-4984-adc3-1c13e5447c19)
 Call ID: cc9370f2-e6ca-4984-adc3-1c13e5447c19
  Args:
    target: Prince_Carlos_of_Bourbon-Parma
    source: Princess_Carolina_of_Bourbon-Parma
    relation: :isSiblingOf
  AddTriple (fc404b89-c59e-408b-bc1a-81bdc2cd536e)
 Call ID: fc404b89-c59e-408b-bc1a-81bdc2cd536e
  Args:
    target: Prince_Jaime_of_Bourbon-Parma
    source: Princess_Carolina_of_Bourbon-Parma
    relation: :isSiblingOf
  AddTriple (05888c3c-8789-4a16-a1d0-8a9096de8aa1)
 Call ID: 05888c3c-8789-4a16-a1d0-8a9096de8aa1
  Args:
    target: Princess_Margarita_of_Bourbon-Parma
    source: Princess_Carolina_of_Bourbon-Parma
    relation: :isSiblingOf
  AssignClass (42331b58-d5a6-49c8-9121-bccf9efefac5)
 Call ID: 42331b58-d5a6-49c8-9121-bccf9efefac5
  Args:
    source: Queen_Juliana_of_the_Netherlands
    type: :Woman
  AssignClass (4fbd47be-f1f9-4d87-9b8e-a4d87a095be9)
 Call ID: 4fbd47be-f1f9-4d87-9b8e-a4d87a095be9
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AddTriple (71ba2f38-80ec-45fc-99d0-2c708d00438f)
 Call ID: 71ba2f38-80ec-45fc-99d0-2c708d00438f
  Args:
    relation: :isChildOf
    target: Queen_Juliana_of_the_Netherlands
    source: Princess_Irene_of_the_Netherlands
  AddTriple (08624898-506a-429d-9a3e-0a607e76ad66)
 Call ID: 08624898-506a-429d-9a3e-0a607e76ad66
  Args:
    relation: :isChildOf
    source: Princess_Irene_of_the_Netherlands
    target: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (7c14081e-1d63-4ea2-8d31-5f1bc46096eb)
 Call ID: 7c14081e-1d63-4ea2-8d31-5f1bc46096eb
  Args:
    type: :Man
    source: Albert_Alphons_Ludgerus_Brenninkmeijer
  AddLiteral (2ae6cf98-0573-4de2-9fbc-2c2753e55fd5)
 Call ID: 2ae6cf98-0573-4de2-9fbc-2c2753e55fd5
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Albert_Alphons_Ludgerus_Brenninkmeijer
    literal_value: 1974
  Finish (aa51f36c-f978-46f6-918b-29d82339a393)
 Call ID: aa51f36c-f978-46f6-918b-29d82339a393
  Args: