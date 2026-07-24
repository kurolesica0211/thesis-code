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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



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
  AssignClass (c7b641c9-c96b-44a5-8ab7-2a9ef8eae882)
 Call ID: c7b641c9-c96b-44a5-8ab7-2a9ef8eae882
  Args:
    type: :Man
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (29ce0d83-85c7-4376-bbeb-0f1cd7ad6a27)
 Call ID: 29ce0d83-85c7-4376-bbeb-0f1cd7ad6a27
  Args:
    type: :Person
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (46e79451-b423-462f-96e9-df901303e757)
 Call ID: 46e79451-b423-462f-96e9-df901303e757
  Args:
    relation: :hasBirthYear
    literal_value: 1933
    literal_type: xsd:nonNegativeInteger
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (3fcea835-0ccc-45a1-8443-df00cd8fd8da)
 Call ID: 3fcea835-0ccc-45a1-8443-df00cd8fd8da
  Args:
    relation: :hasDeathYear
    literal_value: 2019
    literal_type: xsd:nonNegativeInteger
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (f585da70-8f92-45d2-af5d-923524590d9a)
 Call ID: f585da70-8f92-45d2-af5d-923524590d9a
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (de7117bd-b957-4c58-94ee-47acd556bb63)
 Call ID: de7117bd-b957-4c58-94ee-47acd556bb63
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AddLiteral (133cb6ff-22d7-403a-a308-48cdcf07221a)
 Call ID: 133cb6ff-22d7-403a-a308-48cdcf07221a
  Args:
    source: Henri_Count_of_Paris
    literal_value: 1908
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
  AddLiteral (cd8e2180-5975-4e89-9842-ab64e416292b)
 Call ID: cd8e2180-5975-4e89-9842-ab64e416292b
  Args:
    literal_value: 1999
    literal_type: xsd:nonNegativeInteger
    relation: :hasDeathYear
    source: Henri_Count_of_Paris
  AssignClass (2e795d38-3cf4-4010-a8d5-a50c42909f88)
 Call ID: 2e795d38-3cf4-4010-a8d5-a50c42909f88
  Args:
    type: :Woman
    source: Princess_Isabelle_of_Orleans-Braganza
  AssignClass (de392161-1ed4-485d-b8f2-536b60f83318)
 Call ID: de392161-1ed4-485d-b8f2-536b60f83318
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orleans-Braganza
  AddTriple (bea13c06-9f13-468c-9fde-ac90f8b265f9)
 Call ID: bea13c06-9f13-468c-9fde-ac90f8b265f9
  Args:
    target: Henri_Count_of_Paris
    relation: :hasFather
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (18f8b9a4-c0d3-47a1-b213-97a7b7327372)
 Call ID: 18f8b9a4-c0d3-47a1-b213-97a7b7327372
  Args:
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans-Braganza
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (07e72735-270d-4d03-a565-7cafcc187f4b)
 Call ID: 07e72735-270d-4d03-a565-7cafcc187f4b
  Args:
    type: :Man
    source: Francois_dOrleans
  AssignClass (3f44796a-d628-44c1-88d6-97e22b348e26)
 Call ID: 3f44796a-d628-44c1-88d6-97e22b348e26
  Args:
    type: :Person
    source: Francois_dOrleans
  AddTriple (b156e9f2-1272-4892-8ba7-8b51462f12d9)
 Call ID: b156e9f2-1272-4892-8ba7-8b51462f12d9
  Args:
    source: Francois_dOrleans
    relation: :isBrotherOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (4a173986-53a6-482f-af79-b84385613674)
 Call ID: 4a173986-53a6-482f-af79-b84385613674
  Args:
    type: :Woman
    source: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (d8b9befc-ee6d-4730-8e9c-f08a280bf616)
 Call ID: d8b9befc-ee6d-4730-8e9c-f08a280bf616
  Args:
    type: :Person
    source: Duchess_Marie_Therese_of_Wurttemberg
  AddLiteral (28d60c9d-37f1-47c3-9414-f235c4efedbd)
 Call ID: 28d60c9d-37f1-47c3-9414-f235c4efedbd
  Args:
    literal_type: xsd:nonNegativeInteger
    literal_value: 1934
    relation: :hasBirthYear
    source: Duchess_Marie_Therese_of_Wurttemberg
  AddTriple (eb22bb40-fe92-4f9c-a4a0-48e1764292f2)
 Call ID: eb22bb40-fe92-4f9c-a4a0-48e1764292f2
  Args:
    relation: :hasRelation
    target: Duchess_Marie_Therese_of_Wurttemberg
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (bee45a72-3926-433e-8766-a0f1e1bc494d)
 Call ID: bee45a72-3926-433e-8766-a0f1e1bc494d
  Args:
    type: :Woman
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AssignClass (6bb001ed-6c4b-49bc-83aa-bd5ec4422579)
 Call ID: 6bb001ed-6c4b-49bc-83aa-bd5ec4422579
  Args:
    type: :Person
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (72a0e0c7-0e9c-4072-b844-97c6209d65b5)
 Call ID: 72a0e0c7-0e9c-4072-b844-97c6209d65b5
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasBirthYear
    literal_value: 1938
    literal_type: xsd:nonNegativeInteger
  AddLiteral (5b77a254-1325-490a-b0ba-a51402922b0c)
 Call ID: 5b77a254-1325-490a-b0ba-a51402922b0c
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasDeathYear
    literal_type: xsd:nonNegativeInteger
    literal_value: 2022
  AddTriple (9743973a-8861-4545-9b9e-a93a2b29f483)
 Call ID: 9743973a-8861-4545-9b9e-a93a2b29f483
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasRelation
    target: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddLiteral (c90a61e2-7fee-423d-bd33-ee82dae5f25a)
 Call ID: c90a61e2-7fee-423d-bd33-ee82dae5f25a
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_value: 1984
    literal_type: xsd:nonNegativeInteger
    relation: :hasMarriageYear
  AssignClass (d2205d05-7d9d-4790-bda3-ade6bf059973)
 Call ID: d2205d05-7d9d-4790-bda3-ade6bf059973
  Args:
    type: :Woman
    source: Marie_dOrleans
  AssignClass (e7aacf5f-3daf-4835-b442-01e8d18a4126)
 Call ID: e7aacf5f-3daf-4835-b442-01e8d18a4126
  Args:
    type: :Person
    source: Marie_dOrleans
  AddTriple (9286079f-d7d6-435b-900d-a960652d2e84)
 Call ID: 9286079f-d7d6-435b-900d-a960652d2e84
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isFatherOf
    target: Marie_dOrleans
  AddTriple (45e80100-de63-42db-8abb-364f12360cbb)
 Call ID: 45e80100-de63-42db-8abb-364f12360cbb
  Args:
    target: Marie_dOrleans
    relation: :isMotherOf
    source: Duchess_Marie_Therese_of_Wurttemberg
  AssignClass (0ea8ebd4-99b7-4a53-9dc2-b68ada8ef4db)
 Call ID: 0ea8ebd4-99b7-4a53-9dc2-b68ada8ef4db
  Args:
    type: :Man
    source: Prince_Gundakar_of_Liechtenstein
  AssignClass (497f5ec0-58cb-4ac7-8713-db0433bf8d9c)
 Call ID: 497f5ec0-58cb-4ac7-8713-db0433bf8d9c
  Args:
    type: :Person
    source: Prince_Gundakar_of_Liechtenstein
  AddTriple (a1e1b19b-87dc-43d0-929b-b2298da29528)
 Call ID: a1e1b19b-87dc-43d0-929b-b2298da29528
  Args:
    source: Marie_dOrleans
    target: Prince_Gundakar_of_Liechtenstein
    relation: :hasRelation
  AssignClass (3534e5f3-101c-42f7-ae51-47022c72affe)
 Call ID: 3534e5f3-101c-42f7-ae51-47022c72affe
  Args:
    type: :Woman
    source: Diane_dOrleans
  AssignClass (4db89483-f9b4-4a38-b714-3fe1deb19e70)
 Call ID: 4db89483-f9b4-4a38-b714-3fe1deb19e70
  Args:
    type: :Person
    source: Diane_dOrleans
  AddTriple (dd93efef-30c3-4201-bc04-0484a976cdf7)
 Call ID: dd93efef-30c3-4201-bc04-0484a976cdf7
  Args:
    source: Diane_dOrleans
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isSisterOf
  AssignClass (62166eda-cfbe-45d1-8954-406288af4e0e)
 Call ID: 62166eda-cfbe-45d1-8954-406288af4e0e
  Args:
    type: :Man
    source: Michel_Count_of_Evreux
  AssignClass (16195e95-5f50-437b-a18d-3b68c5bedc76)
 Call ID: 16195e95-5f50-437b-a18d-3b68c5bedc76
  Args:
    type: :Person
    source: Michel_Count_of_Evreux
  AddTriple (8eced353-72fa-440d-9f46-071f74209cf4)
 Call ID: 8eced353-72fa-440d-9f46-071f74209cf4
  Args:
    source: Michel_Count_of_Evreux
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isBrotherOf
  AssignClass (fe6a33a0-5bbd-46a3-bf67-0e01192c1600)
 Call ID: fe6a33a0-5bbd-46a3-bf67-0e01192c1600
  Args:
    type: :Man
    source: Thibaut_Count_of_La_Marche
  AssignClass (56cb2f53-310b-4559-805e-bacba000ba04)
 Call ID: 56cb2f53-310b-4559-805e-bacba000ba04
  Args:
    type: :Person
    source: Thibaut_Count_of_La_Marche
  AddTriple (55d2d188-c088-437a-9117-1f72dbb83347)
 Call ID: 55d2d188-c088-437a-9117-1f72dbb83347
  Args:
    relation: :isBrotherOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Thibaut_Count_of_La_Marche
  AssignClass (f55ffb30-a696-43be-b5d3-a9aef2b671de)
 Call ID: f55ffb30-a696-43be-b5d3-a9aef2b671de
  Args:
    type: :Man
    source: Prince_Jacques_Duke_of_Orleans
  AssignClass (81fab4be-8c74-435e-ae73-62d93528a168)
 Call ID: 81fab4be-8c74-435e-ae73-62d93528a168
  Args:
    type: :Person
    source: Prince_Jacques_Duke_of_Orleans
  AddTriple (a76b8672-d77e-42be-86bd-8941484ec4c7)
 Call ID: a76b8672-d77e-42be-86bd-8941484ec4c7
  Args:
    source: Prince_Jacques_Duke_of_Orleans
    relation: :isBrotherOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (b369ded9-509a-4681-9195-8074f684ec73)
 Call ID: b369ded9-509a-4681-9195-8074f684ec73
  Args:
    type: :Man
    source: Prince_Charles-Louis_dOrleans
  AssignClass (1b92ffd9-69ad-402b-b0d5-7454da606431)
 Call ID: 1b92ffd9-69ad-402b-b0d5-7454da606431
  Args:
    type: :Person
    source: Prince_Charles-Louis_dOrleans
  AddLiteral (e5c8b225-9831-4e05-a367-599828e1140a)
 Call ID: e5c8b225-9831-4e05-a367-599828e1140a
  Args:
    source: Prince_Charles-Louis_dOrleans
    literal_type: xsd:nonNegativeInteger
    literal_value: 1972
    relation: :hasBirthYear
  AddTriple (e38f08cb-c53b-41cc-91db-a511d999bbc8)
 Call ID: e38f08cb-c53b-41cc-91db-a511d999bbc8
  Args:
    relation: :isSonOf
    target: Prince_Jacques_Duke_of_Orleans
    source: Prince_Charles-Louis_dOrleans
  AssignClass (f88739e7-fcda-48b5-88f9-002e23a10a47)
 Call ID: f88739e7-fcda-48b5-88f9-002e23a10a47
  Args:
    type: :Man
    source: Prince_Foulques_dOrleans
  AssignClass (548ca85d-ce14-4273-9115-7d8c1c546fbc)
 Call ID: 548ca85d-ce14-4273-9115-7d8c1c546fbc
  Args:
    type: :Person
    source: Prince_Foulques_dOrleans
  AddLiteral (51fcb2a3-6333-47fa-b395-888e7d259f71)
 Call ID: 51fcb2a3-6333-47fa-b395-888e7d259f71
  Args:
    source: Prince_Foulques_dOrleans
    literal_value: 1974
    literal_type: xsd:nonNegativeInteger
    relation: :hasBirthYear
  AddTriple (dd1ef89a-9a74-4de6-93b8-7a2bce4f0eeb)
 Call ID: dd1ef89a-9a74-4de6-93b8-7a2bce4f0eeb
  Args:
    source: Prince_Foulques_dOrleans
    target: Prince_Jacques_Duke_of_Orleans
    relation: :isSonOf
  AssignClass (e721671a-ee30-4b70-8ba5-ef7c0b094092)
 Call ID: e721671a-ee30-4b70-8ba5-ef7c0b094092
  Args:
    type: :Man
    source: Francois_Count_of_Clermont
  AssignClass (95e07827-4b66-4170-a233-afff9f400df5)
 Call ID: 95e07827-4b66-4170-a233-afff9f400df5
  Args:
    type: :Person
    source: Francois_Count_of_Clermont
  AddTriple (74cc6a2b-5e0c-480f-925b-b15fa4d748a2)
 Call ID: 74cc6a2b-5e0c-480f-925b-b15fa4d748a2
  Args:
    relation: :isSonOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Francois_Count_of_Clermont
  AddTriple (61f43d2b-5f65-418c-b2e3-3fecff2c97df)
 Call ID: 61f43d2b-5f65-418c-b2e3-3fecff2c97df
  Args:
    relation: :isSonOf
    target: Duchess_Marie_Therese_of_Wurttemberg
    source: Francois_Count_of_Clermont
  AssignClass (919b0562-bc5b-4d4c-8049-f8da63ec8ca2)
 Call ID: 919b0562-bc5b-4d4c-8049-f8da63ec8ca2
  Args:
    type: :Man
    source: Prince_Jean_Duke_of_Vendome
  AssignClass (550db289-4707-4297-a846-ad2eb4129701)
 Call ID: 550db289-4707-4297-a846-ad2eb4129701
  Args:
    type: :Person
    source: Prince_Jean_Duke_of_Vendome
  AddTriple (6d867d0a-8fc2-40d6-8d3e-507dc994490b)
 Call ID: 6d867d0a-8fc2-40d6-8d3e-507dc994490b
  Args:
    target: Francois_Count_of_Clermont
    relation: :isBrotherOf
    source: Prince_Jean_Duke_of_Vendome
  AssignClass (ae077156-0ed9-40bb-acef-55e9e25b2fa0)
 Call ID: ae077156-0ed9-40bb-acef-55e9e25b2fa0
  Args:
    type: :Man
    source: Luis_Cousino_y_Sebire
  AssignClass (9cc0564d-0188-45bb-abe0-ecc0680255aa)
 Call ID: 9cc0564d-0188-45bb-abe0-ecc0680255aa
  Args:
    type: :Person
    source: Luis_Cousino_y_Sebire
  AssignClass (2607a81e-6285-4d44-b1d5-32943886d515)
 Call ID: 2607a81e-6285-4d44-b1d5-32943886d515
  Args:
    type: :Woman
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AssignClass (bc5b91a3-60f2-4f4c-9665-86976a538a91)
 Call ID: bc5b91a3-60f2-4f4c-9665-86976a538a91
  Args:
    type: :Person
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AddTriple (b8b6ce2e-7062-41ce-8a8b-b201c2b44bc2)
 Call ID: b8b6ce2e-7062-41ce-8a8b-b201c2b44bc2
  Args:
    target: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :isFatherOf
    source: Luis_Cousino_y_Sebire
  AddTriple (25b7cb0a-9db3-4402-be67-c5ee7505ba27)
 Call ID: 25b7cb0a-9db3-4402-be67-c5ee7505ba27
  Args:
    target: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :isMotherOf
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AssignClass (141d00a5-330f-41b8-a17d-75d6b525d738)
 Call ID: 141d00a5-330f-41b8-a17d-75d6b525d738
  Args:
    type: :Man
    source: Jean-Robert_Boeuf
  AssignClass (03b9e72a-a8e4-40f4-bcbf-9fb3282ac182)
 Call ID: 03b9e72a-a8e4-40f4-bcbf-9fb3282ac182
  Args:
    type: :Person
    source: Jean-Robert_Boeuf
  AddTriple (f325f0e7-cf90-4733-b0f8-1ef601185e12)
 Call ID: f325f0e7-cf90-4733-b0f8-1ef601185e12
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasRelation
    target: Jean-Robert_Boeuf
  Finish (5f652c64-0313-40c1-bfa5-12afa8adcc31)
 Call ID: 5f652c64-0313-40c1-bfa5-12afa8adcc31
  Args: